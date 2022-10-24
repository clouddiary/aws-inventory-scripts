#
# Script Creates Spread Sheet containing all information about ALB(V1 & V2) in a specific AWS account.
#
# AWS CLI profile needs to be created on machine where script will run & pass profile name.

import boto3
import json
import xlsxwriter
import sys

profile_name='qa'
xlsx_filename='Combined-ALB-Inventory.xlsx'

session = boto3.Session(profile_name=profile_name)
albv1 = session.client('elb')
alb = session.client('elbv2')



Next_Token = None

#
# Create the Spread Sheet
#
workbook = xlsxwriter.Workbook(xlsx_filename)
bold = workbook.add_format({'bold': True})
row = 0
SheetName = 'ALB Info'
worksheet = workbook.add_worksheet('ALBs')
worksheet.write(row, 0, 'LB Name', bold)
worksheet.write(row, 1, 'DNSName', bold)
worksheet.write(row, 2, 'LoadBalancerArn', bold)
worksheet.write(row, 3, 'VPCID', bold)

row += 1

while True:
    
    paginator = albv1.get_paginator('describe_load_balancers')
    print("HelloOOOOOOOOOOOOOOOOOOO: ",Next_Token)
    response_iterator = paginator.paginate(
        PaginationConfig={
                'MaxItems': 300,
                'PageSize': 100,
                'StartingToken': Next_Token}
    )

    for page in response_iterator:
        lbs = page['LoadBalancerDescriptions']
        
        
        for lb in lbs:
            
            worksheet.write(row, 0, lb['LoadBalancerName'])
            try:
                print(lb['DNSName'])
                worksheet.write(row, 1,lb['DNSName'])
                #worksheet.write(row, 2,lb['LoadBalancerArn'])
                worksheet.write(row, 3,lb['VPCId'])
                
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
#

Next_Token = None
while True:
    
    paginator = alb.get_paginator('describe_load_balancers')
    print("HelloOOOOOOOOOOOOOOOOOOO: ",Next_Token)
    response_iterator = paginator.paginate(
        PaginationConfig={
                'MaxItems': 300,
                'PageSize': 100,
                'StartingToken': Next_Token}
    )

    for page in response_iterator:
        lbs = page['LoadBalancers']
        
        
        for lb in lbs:
            
            worksheet.write(row, 0, lb['LoadBalancerName'])
            try:
                print(lb['DNSName'])
                worksheet.write(row, 1,lb['DNSName'])
                worksheet.write(row, 2,lb['LoadBalancerArn'])
                worksheet.write(row, 3,lb['VpcId'])
                
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