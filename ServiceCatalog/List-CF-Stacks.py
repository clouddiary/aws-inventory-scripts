import boto3
import json
import xlsxwriter
import sys


# aws cloudformation list-stacks --query "StackSummaries[*].[StackId,StackName]" --output text > All-Stack-ids.txt

session = boto3.Session(profile_name='qa')
client = session.client('cloudformation')

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

row += 1
#paginator = client.get_paginator('list_stacks')
marker = None
while True:
    paginator = client.get_paginator('list_stacks')
    response_iterator = paginator.paginate(
        PaginationConfig={
            'MaxItems': 10,
            'StartingToken': marker})
    for page in response_iterator:
        #print("Next Page : {} ".format(page['IsTruncated']))
        #print(page)
        u = page['StackSummaries']
        for user in u:
            row += 1
            print(user['StackName'])
            worksheet.write(row, 0, user['StackName'])
            worksheet.write(row, 1, user['StackId'])
            stack_details = client.describe_stacks(StackName=user['StackId'])
            print(stack_details['Stacks'][0]['StackName'],stack_details['Stacks'][0]['Tags'])
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
    try:
            
        marker = page['NextToken']
        #print(marker)
    except KeyError:
        workbook.close()
        print("Inventory is created")
        sys.exit()



