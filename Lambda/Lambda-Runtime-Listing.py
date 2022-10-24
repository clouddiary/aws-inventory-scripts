#
# Script pulls all lambda functions in an aws account along with runtime details
#
# AWS CLI profile needs to be created on machine where script will run & pass profile name.
import boto3
import json
import xlsxwriter
import sys

## Update local aws cli profile name here
session = boto3.Session(profile_name='qa')
lamb = session.client('lambda')


Next_Token = None

#
# Create the Spread Sheet
#
workbook = xlsxwriter.Workbook('Lambdas-Runtime.xlsx')
bold = workbook.add_format({'bold': True})
row = 0
SheetName = 'Lambda'
worksheet = workbook.add_worksheet('Lambdas')
worksheet.write(row, 0, 'Lambda Name', bold)
worksheet.write(row, 1, 'Runtime', bold)
row += 1
while True:
    paginator = lamb.get_paginator('list_functions')
    print("HelloOOOOOOOOOOOOOOOOOOO: ",Next_Token)
    response_iterator = paginator.paginate(
        PaginationConfig={
                'MaxItems': 300,
                'PageSize': 100,
                'StartingToken': Next_Token}
    )

    for page in response_iterator:
        #print(page)
        functions = page['Functions']
        for function in functions:
            print(function['FunctionName'])
            worksheet.write(row, 0, function['FunctionName'])
            worksheet.write(row, 1, function['Runtime'])
            row += 1

    try:
        Next_Token = page['NextMarker']
        print("Next Token is: ",Next_Token)
    except KeyError:
    #    sys.exit()
        break


workbook.close()
print("Inventory is created")