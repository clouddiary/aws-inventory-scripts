#
# Script gets all VPC changes from AWS Configs
#
# AWS CLI profile needs to be created on machine where script will run & pass profile name.
import sys
import boto3
from datetime import datetime
import argparse
import xlsxwriter
 
session = boto3.Session(profile_name='qa')
config = session.client("config", verify=False)

Next_Token = None
while True:
    paginator = config.get_paginator('get_resource_config_history')
    print("HelloOOOOOOOOOOOOOOOOOOO: ",Next_Token)
    response_iterator = paginator.paginate(
        resourceType='AWS::EC2::VPC',
        resourceId='vpc-id-12345',
        earlierTime=datetime(2022, 4, 7),
        chronologicalOrder='Forward',
        PaginationConfig={
            'MaxItems': 1,
            'PageSize': 100,
            'StartingToken': Next_Token}
    )
    for page in response_iterator:
        #print("Next Page : {} ".format(page['IsTruncated']))
        print(page)
        config_items = page['configurationItems']
        for item in config_items:
            print(item['arn'])
        try:
            marker = page['Marker']
            Next_Token = page['nextToken']
            #print(Next_Token)
        except KeyError:
            sys.exit()