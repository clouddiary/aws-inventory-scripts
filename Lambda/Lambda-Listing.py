#
# Script pulls all lambda functions in an aws account along with its security grousp & subnets
#
# AWS CLI profile needs to be created on machine where script will run & pass profile name.

import boto3
import json
import xlsxwriter
import sys

## Update local aws cli profile name here
session = boto3.Session(profile_name='qa')
lam = session.client('lambda')


Next_Token = None

#
# Create the Spread Sheet
#
workbook = xlsxwriter.Workbook('List-Lambda.xlsx')
bold = workbook.add_format({'bold': True})
row = 0
SheetName = 'EC2 Instances'
worksheet = workbook.add_worksheet('Lambdas')
worksheet.write(row, 0, 'Lambda Name', bold)
worksheet.write(row, 1, 'VPC ID', bold)
worksheet.write(row, 2, 'SubnetIds', bold)
worksheet.write(row, 3, 'SecurityGroupIds', bold)
row += 1
while True:
    paginator = lam.get_paginator('list_functions')
    print("HelloOOOOOOOOOOOOOOOOOOO: ",Next_Token)
    response_iterator = paginator.paginate(
        PaginationConfig={
                'MaxItems': 300,
                'PageSize': 100,
                'StartingToken': Next_Token}
    )

    for page in response_iterator:
        functions = page['Functions']
        for function in functions:
            print(function['FunctionName'])
            worksheet.write(row, 0, function['FunctionName'])
            try:
                print(function['VpcConfig'])
                worksheet.write(row, 1,function['VpcConfig']['VpcId'])
                worksheet.write(row, 2,', '.join(function['VpcConfig']['SubnetIds']))
                worksheet.write(row, 3,', '.join(function['VpcConfig']['SecurityGroupIds']))
            except KeyError:
                print()
                worksheet.write(row, 1,"")
            row += 1

    try:
        Next_Token = page['nextToken']
        print(Next_Token)
    except KeyError:
    #    sys.exit()
        break


workbook.close()
print("Inventory is created")