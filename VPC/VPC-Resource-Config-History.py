#
# Script gets all VPC changes from AWS Configs
#
# AWS CLI profile needs to be created on machine where script will run & pass profile name.

import sys
import boto3
from datetime import datetime
import argparse
import xlsxwriter

workbook = xlsxwriter.Workbook('VPC-Changes-log.xlsx',{'remove_timezone': True})
bold = workbook.add_format({'bold': True})
worksheet = workbook.add_worksheet('VPC')

time_format = workbook.add_format({'num_format': 'dd/mm/yy hh:mm'})

row = 0

version = 0
accountId = 1
configurationItemCaptureTime = 2
configurationItemStatus = 3
configurationStateId = 4
configurationItemMD5Hash = 5
arn = 6
resourceType = 7
resourceId = 8
resourceName = 9
awsRegion = 10
availabilityZone = 11
resourceCreationTime = 12
relatedEvents = 13
relationships = 14
configuration = 15

worksheet.write(row, version, 'version', bold)
worksheet.write(row, accountId, 'accountId', bold)
worksheet.write(row, configurationItemCaptureTime, 'configurationItemCaptureTime', bold)
worksheet.write(row, configurationItemStatus, 'configurationItemStatus', bold)
worksheet.write(row, configurationStateId, 'configurationStateId', bold)
worksheet.write(row, arn, 'arn', bold)
worksheet.write(row, resourceType, 'resourceType', bold)
worksheet.write(row, resourceId, 'resourceId', bold)
worksheet.write(row, resourceName, 'resourceName', bold)
worksheet.write(row, awsRegion, 'awsRegion', bold)
worksheet.write(row, availabilityZone, 'availabilityZone', bold)
worksheet.write(row, resourceCreationTime, 'resourceCreationTime', bold)
worksheet.write(row, relatedEvents, 'relatedEvents', bold)
worksheet.write(row, relationships, 'relationships', bold)
worksheet.write(row, configuration, 'configuration', bold)



APPLICABLE_RESOURCES = ["AWS::IAM::User","AWS::EC2::VPC"]
## Update local aws cli profile name here
session = boto3.Session(profile_name='qa')
config = session.client("config")

marker = None
while True:
    paginator = config.get_paginator('get_resource_config_history')
    response_iterator = paginator.paginate(
        resourceType='AWS::EC2::VPC',
        resourceId='vpc-id-12345',
        earlierTime=datetime(2020, 4, 7),
        chronologicalOrder='Forward',
        PaginationConfig={
            'MaxItems': 100,
            'PageSize': 100,
            'StartingToken': marker
    }
    )
    #print(marker)
    for page in response_iterator:
        #print("Next Page : {} ".format(page['IsTruncated']))
        print(page)
        config_items = page['configurationItems']
        for item in config_items:
            row += 1
            print("Row: ",row, item['version'])
            worksheet.write(row, version, item['version'])
            worksheet.write(row, accountId, item['accountId'])
            worksheet.write(row, configurationItemCaptureTime, item['configurationItemCaptureTime'], time_format)
            worksheet.write(row, configurationItemStatus, item['configurationItemStatus'])
            worksheet.write(row, configurationStateId, item['configurationStateId'])
            worksheet.write(row, arn, item['arn'])
            worksheet.write(row, resourceType, item['resourceType'])
            worksheet.write(row, resourceId, item['resourceId'])
            try:
                worksheet.write(row, resourceName, item['resourceName'])
            except:
                worksheet.write(row, resourceName, "")
            worksheet.write(row, awsRegion, item['awsRegion'])
            worksheet.write(row, availabilityZone, item['availabilityZone'])
            try:
                worksheet.write(row, resourceCreationTime, item['resourceCreationTime'], time_format)
            except:
                worksheet.write(row, resourceCreationTime, "")

            worksheet.write(row, relatedEvents, ''.join(map(str, item['relatedEvents'])))
            worksheet.write(row, relationships, ''.join(map(str, item['relationships'])))
            worksheet.write(row, configuration, item['configuration'])
            #print(item['NextToken'])
    #print(page['Marker'])
        try:
            marker = page['nextToken']
            #print(page['nextToken'])
            print("Marker :",marker)
        except KeyError:
            print("Closing WorkBook")
            workbook.close()
            sys.exit()