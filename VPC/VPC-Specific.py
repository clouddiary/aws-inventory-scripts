import sys
import boto3
from datetime import datetime
import argparse
import xlsxwriter
 
#s3 = boto3.client('config')
#print(s3.can_paginate('get_resource_config_history')) # =&gt; True



session = boto3.Session(profile_name='qa')
ec2 = session.client("ec2")
config = session.client("config")
ec2 = session.resource('ec2')
vpc = ec2.Vpc('vpc-id-12345S')
security_group_iterator = vpc.security_groups.all()
for sc in security_group_iterator:
    print(sc.group_id)

route_table_iterator = vpc.route_tables.all()
for rt in route_table_iterator:
    print(rt.route_table_id)

subnet_iterator = vpc.subnets.all()
for sn in subnet_iterator:
    print(sn.subnet_id)


'''

Out_Next_Token = ""
while True:
    response = ec2.describe_security_groups(NextToken=Out_Next_Token)
    
    for sc in response['SecurityGroups']:
        print(sc['GroupId'])
        if sc['GroupId'] == ""
        In_Next_Token = ""
        while True:
            response1 = config.get_resource_config_history(resourceType='AWS::EC2::SecurityGroup', resourceId=sc['GroupId'], earlierTime=datetime(2020, 4, 7), chronologicalOrder='Forward', limit=100, nextToken=In_Next_Token)
            for item in response1['configurationItems']:
                print(item['configuration'])
                if item['configurationItemStatus'] == "ResourceDiscovered":
                    print(item['configuration'],"###########################HELLO############################")
            try:
                In_Next_Token=response1['nextToken']
            except KeyError:
                print("")
    try:
        Out_Next_Token=response['NextToken']
        print(Out_Next_Token)
    except KeyError:
        sys.exit()

'''