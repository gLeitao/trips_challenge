import boto3
import os
import sys
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--path", required=True)
args = parser.parse_args()

if not os.path.exists(args.path):
    raise ValueError(f"The file path does not exist: {args.path}")
    
session = boto3.Session()
s3 = session.client('s3', 
                    region_name='us-east-2', 
                    config=boto3.session.Config(signature_version='s3v4'),
                    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

try:
    with open(args.path, 'rb') as f:
        s3.upload_fileobj(f, 'trips-datalake', f'landing/trips/datetime={date}/trips.csv') 
except Exception as e:
        print("Error uploading file to S3: {}".format(str(e)))   


client = boto3.client('glue')

client.start_job_run(JobName = 'raw_job',
                     Arguments = { '--datetime':  date} )