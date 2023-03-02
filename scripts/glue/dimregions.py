import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from datetime import datetime
import os
import delta 

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'datetime'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init('move_raw', args)
job.commit()

spark.conf.set("spark.sql.sources.partitionOverwriteMode","dynamic")
  
df = (spark.read 
           .format('parquet')
           .load(f"s3://trips-datalake/raw/trips/datetime={args['datetime']}")
     )
df.createOrReplaceTempView('vw_trips')

sql_dimregions = '''
select sha2(lower(region), 256) as cdregion, region
from vw_trips
group by region
'''

df_dim_regions = spark.sql(sql_dimregions)

try:
  df_dim_regions_table = delta.tables.DeltaTable.forPath(spark, "s3://trips-datalake/business/trips/dimregions")
except Exception as e:
  df_dim_regions.write.format("delta").save("s3://trips-datalake/business/trips/dimregions")
  os._exit(0)

(df_dim_regions_table.alias("target")
  .merge(source = df_dim_regions.alias("source"), condition = "source.region = target.region") 
  .whenNotMatchedInsertAll() 
  .execute()
)