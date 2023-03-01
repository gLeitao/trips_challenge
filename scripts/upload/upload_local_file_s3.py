import boto3
import os
import sys
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--path", required=True)
args = parser.parse_args()
    
session = boto3.Session()
s3 = session.client('s3', 
                    region_name='us-east-2', 
                    config=boto3.session.Config(signature_version='s3v4'),
                    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(args.path, 'rb') as f:
    s3.upload_fileobj(f, 'datalake-geovani-igti', f'datetime={date}/trips.csv') 