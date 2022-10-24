#
# Script fetches all API Gateway with their WAF details 
#
# AWS CLI profile needs to be created on machine where script will run & pass profile name.

import sys
import boto3
from datetime import datetime
import argparse
import xlsxwriter
import json
from botocore.exceptions import ClientError

xlsx_filename='TEZS-WAF-Info-05042021.xlsx'
profile_name='qa'
session = boto3.Session(profile_name=profile_name)
client = session.client('apigateway')

workbook = xlsxwriter.Workbook(xlsx_filename)
bold = workbook.add_format({'bold': True})
row = 0
SheetName = 'API Info'
worksheet = workbook.add_worksheet('APIInfo')
worksheet.write(row, 0, 'DomainID', bold)
worksheet.write(row, 1, 'Name', bold)
worksheet.write(row, 2, 'Stage', bold)
worksheet.write(row, 3, 'WAF', bold)

row += 1

Next_Token = None
paginator = client.get_paginator('get_rest_apis')

while True:
    
    response_iterator = paginator.paginate(
        PaginationConfig={
            'MaxItems': 100,
            'PageSize': 100,
            'StartingToken': Next_Token
        }
    )
    for page in response_iterator:
        #api_items = page['items']
        for item in page['items']:
            print(item['id'],item['name'])
            worksheet.write(row, 0, item['id'])
            worksheet.write(row, 1, item['name'])
            response = client.get_stages(restApiId=item['id'])
            for stage in response['item']:
                print(stage['deploymentId'],stage['stageName'])
                try:
                    response2 = client.get_stage(restApiId=item['id'],stageName=stage['stageName'])
                    worksheet.write(row, 2, stage['stageName'])
                    worksheet.write(row, 3, response2['webAclArn'])
                except KeyError:
                    print("No WAF")
                    worksheet.write(row, 3, "No WAF")
            row += 1     
        try:
            Next_Token = page['nextToken']
            print(Next_Token)
        except KeyError:
            workbook.close()
            sys.exit()

workbook.close()