#
# Script scans all SGs & discovers SG changes in AWS config
#
# AWS CLI profile needs to be created on machine where script will run & pass profile name.

import sys
import boto3
from datetime import datetime
import argparse
import xlsxwriter
 
#s3 = boto3.client('config')
#print(s3.can_paginate('get_resource_config_history')) # =&gt; True


## Update local aws cli profile name here
session = boto3.Session(profile_name='qa')
#ec2 = session.client("ec2")
config = session.client("config")
ec2 = session.resource('ec2')

## Update vpc id here
vpc = ec2.Vpc('vpc-id-1234')

security_group_iterator = vpc.security_groups.all()
for sc in security_group_iterator:
    print(sc.group_id)
    In_Next_Token = ""
    while True:
        # Update date based on filter criteria
        response1 = config.get_resource_config_history(resourceType='AWS::EC2::SecurityGroup', resourceId=sc.group_id, earlierTime=datetime(2020, 4, 7), chronologicalOrder='Forward', limit=100, nextToken=In_Next_Token)
        for item in response1['configurationItems']:
            #print(item['configuration'])
            print(item['arn'])
            if item['configurationItemStatus'] == "ResourceDiscovered":
                print(item['configuration'],"###########################HELLO############################")
        try:
            In_Next_Token=response1['nextToken']
        except KeyError:
            print("")
    