import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from datetime import datetime
import os
import delta
import boto3
import json

args = getResolvedOptions(sys.argv, ["JOB_NAME", "datetime", "hashid"])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init("move_raw", args)
job.commit()

spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")


def insert_status(comments):
    try:
        df_control = spark.createDataFrame(
            [(args["hashid"], datetime.now(), comments)],
            ["hashid", "datetime", "comments"],
        )

        print(df_control.show())

        client = boto3.client("secretsmanager", region_name="us-east-2")
        get_secret_value_response = client.get_secret_value(SecretId="dev/trips-db")
        secret = json.loads(get_secret_value_response["SecretString"])

        (
            df_control.write.format("jdbc")
            .option("url", secret.get("host"))
            .option("dbtable", "control.trips_load")
            .option("user", secret.get("username"))
            .option("password", secret.get("password"))
            .mode("append")
            .save()
        )
    except Exception as e:
        raise ValueError(
            f"Error when trying to salve data into data control process: {e}"
        )


insert_status("Running Dim Layer - DIMDATASOURCES")

df = spark.read.format("parquet").load(
    f"s3://trips-datalake/raw/trips/datetime={args['datetime']}"
)
df.createOrReplaceTempView("vw_trips")

sql_dimdatasources = """
select sha2(lower(datasource), 256) as cddatasource, datasource
from vw_trips
group by datasource
"""

df_dim_datasources = spark.sql(sql_dimdatasources)

try:
    df_dim_datasources_table = delta.tables.DeltaTable.forPath(
        spark, "s3://trips-datalake/business/trips/dimdatasources"
    )
except Exception as e:
    df_dim_datasources.write.format("delta").save(
        "s3://trips-datalake/business/trips/dimdatasources"
    )
    os._exit(0)

(
    df_dim_datasources_table.alias("target")
    .merge(
        source=df_dim_datasources.alias("source"),
        condition="source.datasource = target.datasource",
    )
    .whenNotMatchedInsertAll()
    .execute()
)

try:
    client = boto3.client("secretsmanager", region_name="us-east-2")
    get_secret_value_response = client.get_secret_value(SecretId="dev/trips-db")
    secret = json.loads(get_secret_value_response["SecretString"])

    (
        df_dim_datasources_table.toDF()
        .write.format("jdbc")
        .option("url", secret.get("host"))
        .option("dbtable", "trips.dimdatasources")
        .option("user", secret.get("username"))
        .option("password", secret.get("password"))
        .mode("overwrite")
        .save()
    )
except Exception as e:
    insert_status("Error when trying to salve data into redshift - DIMDATASOURCES")
    raise ValueError(f"Error when trying to salve data into redshift: {e}")
