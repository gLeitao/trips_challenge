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

def insert_redshift(df_insert, table, method):
    try:
        client = boto3.client("secretsmanager", region_name="us-east-2")
        get_secret_value_response = client.get_secret_value(SecretId="dev/trips-db")
        secret = json.loads(get_secret_value_response["SecretString"])
    
        (
            df_insert.write.format("jdbc")
            .option("url", secret.get("host"))
            .option("dbtable", table)
            .option("user", secret.get("username"))
            .option("password", secret.get("password"))
            .mode(method)
            .save()
        )
    except Exception as e:
        raise ValueError("Error when trying to salve data into redshift")

def insert_status(comments): 
    df_control = spark.createDataFrame(
        [(args["hashid"], datetime.now(), comments)],
        ["hashid", "datetime", "comments"],
    )
    
    insert_redshift(df_control, "control.trips_load", "append")


insert_status("Running Fact Layer")

df = spark.read.format("parquet").load(
    f"s3://trips-datalake/raw/trips/datetime={args['datetime']}"
)
df.createOrReplaceTempView("vw_trips")


df_dim_regions_table = delta.tables.DeltaTable.forPath(
    spark, "s3://trips-datalake/business/trips/dimregions"
)
df_dim_regions_table.toDF().createOrReplaceTempView("vw_dimregions")

df_dim_dimdatasources_table = delta.tables.DeltaTable.forPath(
    spark, "s3://trips-datalake/business/trips/dimdatasources"
)
df_dim_dimdatasources_table.toDF().createOrReplaceTempView("vw_dimdatasources")


sql_factrips = """
select reg.cdregion,
       dts.cddatasource, 
       date_trunc('hour', trps.datetime) as datetime,
       count(*) as count_trips
from vw_trips trps
left join vw_dimregions reg on lower(trps.region) = lower(reg.region)
left join vw_dimdatasources dts on lower(trps.datasource) = lower(dts.datasource)
group by reg.cdregion, 
         dts.cddatasource, 
         date_trunc('hour', trps.datetime) 
"""

df_fact_trips = spark.sql(sql_factrips)

try:
    df_fact_trips_table = delta.tables.DeltaTable.forPath(
        spark, "s3://trips-datalake/business/trips/facttrips"
    )
except Exception as e:
    df_fact_trips.write.format("delta").save(
        "s3://trips-datalake/business/trips/facttrips"
    )
    insert_redshift(df_fact_trips, "trips.facttrips", "overwrite")
    insert_status("Facttrips Layer runs successfully!")
    os._exit(0)

(
    df_fact_trips_table.alias("target")
    .merge(
        source=df_fact_trips.alias("source"),
        condition="source.cdregion = target.cdregion and source.cddatasource = target.cddatasource and source.datetime = target.datetime",
    )
    .whenNotMatchedInsertAll()
    .whenMatchedUpdate(set={"count_trips": "target.count_trips + source.count_trips"})
    .execute()
)

insert_redshift(df_fact_trips_table.toDF(), "trips.facttrips", "overwrite")

insert_status("Fact Layer runs successfully!")