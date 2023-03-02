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


df_dim_regions_table = delta.tables.DeltaTable.forPath(spark, "s3://trips-datalake/business/trips/dimregions")
df_dim_regions_table.toDF().createOrReplaceTempView('vw_dimregions')

df_dim_dimdatasources_table = delta.tables.DeltaTable.forPath(spark, "s3://trips-datalake/business/trips/dimdatasources")
df_dim_dimdatasources_table.toDF().createOrReplaceTempView('vw_dimdatasources')



sql_factrips = '''
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
'''

df_fact_trips = spark.sql(sql_factrips)

try:
  df_fact_trips_table = delta.tables.DeltaTable.forPath(spark, "s3://trips-datalake/business/trips/factrips")
except Exception as e:
  df_fact_trips.write.format("delta").save("s3://trips-datalake/business/trips/factrips")
  os._exit(0)

(df_fact_trips_table.alias("target")
  .merge(source = df_fact_trips.alias("source"), condition = "source.cdregion = target.cdregion and source.cddatasource = target.cddatasource and source.datetime = target.datetime") 
  .whenNotMatchedInsertAll() 
  .whenMatchedUpdate(set =
    {
      "count_trips": "target.count_trips + source.count_trips"
    }
  )
  .execute()
)