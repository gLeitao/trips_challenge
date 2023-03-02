import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from datetime import datetime

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'datetime'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init('move_raw', args)
job.commit()

spark.conf.set("spark.sql.sources.partitionOverwriteMode","dynamic")

df = (spark.read
           .format("csv") 
           .option("inferSchema", True) 
           .option("header", True) 
           .option("sep", ",") 
           .load(f"s3://trips-datalake/landing/trips/datetime={args['datetime']}/")
     )
   
(df.write
  .mode('overwrite')
  .format('parquet')
  .save(f"s3://trips-datalake/raw/trips/datetime={args['datetime']}")
)