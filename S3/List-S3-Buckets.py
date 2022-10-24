#
# Script pulls all s3 buckets in an aws account
#
# AWS CLI profile needs to be created on machine where script will run & pass profile name.

import boto3
from botocore.exceptions import ClientError
import json
import xlsxwriter
import sys

row = 1
# Initailizing account from which we need to generate report.
session = boto3.Session(profile_name='qa')
client = session.client('s3')
response = client.list_buckets()
for bucket in response['Buckets']:
    bucketName = bucket['Name']
    print(row, " : ",bucketName)
    row +=1