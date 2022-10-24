#
# Script pulls list of IAM groups in an AWS account along with their users.
#
# AWS CLI profile needs to be created on machine where script will run & pass profile name.

import boto3
import json
import xlsxwriter
import sys

## Update local aws cli profile name here
session = boto3.Session(profile_name='qa')
lam = session.client('iam')
iam = session.resource('iam')


Next_Token = None

#
# Create the Spread Sheet
#
workbook = xlsxwriter.Workbook('List-IAMGroup.xlsx')
bold = workbook.add_format({'bold': True})
row = 0
SheetName = 'EC2 Instances'
worksheet = workbook.add_worksheet('IAMGroup')
worksheet.write(row, 0, 'Group Name', bold)
worksheet.write(row, 1, 'GroupID', bold)
worksheet.write(row, 2, 'Arn', bold)
worksheet.write(row, 3, 'Users', bold)
row += 1
while True:
    paginator = lam.get_paginator('list_groups')
    print("HelloOOOOOOOOOOOOOOOOOOO: ",Next_Token)
    response_iterator = paginator.paginate(
        PaginationConfig={
                'MaxItems': 300,
                'PageSize': 100,
                'StartingToken': Next_Token}
    )

    for page in response_iterator:
        groups = page['Groups']
        for group in groups:
            users=[]
            print(group['GroupName'])
            worksheet.write(row, 0, group['GroupName'])
            try:                
                worksheet.write(row, 1,group['GroupId'])
                worksheet.write(row, 2,group['Arn'])
                group2 = iam.Group(group['GroupName'])
                user_iterator = group2.users.all()
                for usr in user_iterator:
                    #print(usr.name)
                    users.append(usr.name)
                worksheet.write(row, 3,', '.join(users))
                
                
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