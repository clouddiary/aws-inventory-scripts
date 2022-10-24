import boto3
import json
import xlsxwriter
import sys


# aws cloudformation list-stacks --query "StackSummaries[*].[StackId,StackName]" --output text > All-Stack-ids.txt

session = boto3.Session(profile_name='qa')
client = session.client('cloudformation')

filepath="All-Stack-ids-Only.txt"
#
# Create the Spread Sheet containing all information about EC2.
#
# Creating Excel worksheet
workbook = xlsxwriter.Workbook('Cloud-Formation-Details.xlsx')

bold = workbook.add_format({'bold': True})
row = 0
worksheet = workbook.add_worksheet('CloudFormation')
worksheet.write(row, 0, 'StackName', bold)
worksheet.write(row, 1, 'StackId', bold)
worksheet.write(row, 2, 'productArn', bold)
worksheet.write(row, 3, 'provisionedProductArn', bold)
worksheet.write(row, 4, 'provisioningPrincipalArn', bold)


#paginator = client.get_paginator('list_stacks')
with open(filepath) as fp:
       cnt = 0
       for line in fp:
           StackName=line.strip()
           try:
            stack_details = client.describe_stacks(StackName=StackName)
            row += 1
            print(stack_details['Stacks'][0]['StackName'],stack_details['Stacks'][0]['Tags'])
            worksheet.write(row, 0, stack_details['Stacks'][0]['StackName'])
            worksheet.write(row, 1, stack_details['Stacks'][0]['StackId'])
            for Tag in stack_details['Stacks'][0]['Tags']:
               #print(Tag['Key'],":",Tag['Value'])
               if 'aws:servicecatalog:productArn'in Tag['Key']:
                   print(Tag['Value'])
                   worksheet.write(row, 2, Tag['Value'])
               if 'aws:servicecatalog:provisionedProductArn'in Tag['Key']:
                   print(Tag['Value'])
                   worksheet.write(row, 3, Tag['Value'])
               if 'aws:servicecatalog:provisioningPrincipalArn'in Tag['Key']:
                   print(Tag['Value'])
                   worksheet.write(row, 4, Tag['Value'])
           except:
                 print(StackName," is not exist")                
workbook.close()
print("Inventory is created")