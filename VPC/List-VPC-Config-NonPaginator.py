#
# Script gets all VPC changes from AWS Configs
#
# AWS CLI profile needs to be created on machine where script will run & pass profile name.

import sys
import boto3
from datetime import datetime
import argparse
import xlsxwriter
 
## Update local aws cli profile name here
session = boto3.Session(profile_name='qa')
config = session.client("config")

Next_Token = ""
while True:
    response = config.get_resource_config_history(
        resourceType='AWS::EC2::VPC',
        resourceId='vpc-id-12345',
        earlierTime=datetime(2022, 4, 7),
        chronologicalOrder='Forward',
        limit=100,
        nextToken=Next_Token
    )
    
    for item in response['configurationItems']:
        #print("Next Page : {} ".format(page['IsTruncated']))
        #print(page)
        #config_items = page['configurationItems']
        #for item in config_items:
        print(item)
    
    try:
        Next_Token=response['nextToken']
        #print(Next_Token)
    except KeyError:
        sys.exit()