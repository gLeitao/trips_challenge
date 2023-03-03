import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from datetime import datetime
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


insert_status("Running Raw Layer")

try:
    df = (
        spark.read.format("csv")
        .option("inferSchema", True)
        .option("header", True)
        .option("sep", ",")
        .load(f"s3://trips-datalake/landing/trips/datetime={args['datetime']}/")
    )
except Exception as e:
    insert_status(f"Error when trying to read data from CSV: {e}")
    raise ValueError(f"Error when trying to read data from CSV: {e}")

try:
    (
        df.write.mode("overwrite")
        .format("parquet")
        .save(f"s3://trips-datalake/raw/trips/datetime={args['datetime']}/")
    )
except Exception as e:
    insert_status(f"Error when trying to salve data into Raw Layer: {e}")
    raise ValueError(f"Error when trying to salve data into Raw Layer: {e}")
