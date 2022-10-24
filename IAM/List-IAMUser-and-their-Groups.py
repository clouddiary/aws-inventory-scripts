#
# Script pulls all IAM users in an account along with their groups in matrix format
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

##
#Gather group names
Group_Names=[]
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
            Group_Names.append(group['GroupName'])
    try:
        Next_Token = page['nextToken']
        print(Next_Token)
    except KeyError:
    #    sys.exit()
        break
Group_Names.sort()
#
# Create the Spread Sheet
#
workbook = xlsxwriter.Workbook('List-IAMUser.xlsx')
bold = workbook.add_format({'bold': True})
row = 0
SheetName = 'EC2 Instances'
worksheet = workbook.add_worksheet('IAMUser')
worksheet.write(row, 0, 'User Name', bold)
#worksheet.write(row, 1, 'UserID', bold)
#worksheet.write(row, 2, 'Arn', bold)
#worksheet.write(row, 3, 'Groups', bold)
row += 1
while True:
    paginator = lam.get_paginator('list_users')
    print("HelloOOOOOOOOOOOOOOOOOOO: ",Next_Token)
    response_iterator = paginator.paginate(
        PaginationConfig={
                'MaxItems': 300,
                'PageSize': 100,
                'StartingToken': Next_Token}
    )

    for page in response_iterator:
        users = page['Users']
        for user in users:
            groups=[]
            #print(user['GroupName'])
            worksheet.write(row, 0, user['UserName'])
            try:                
                #worksheet.write(row, 1,user['UserId'])
                #worksheet.write(row, 2,user['Arn'])
                user2 = iam.User(user['UserName'])
                group_iterator = user2.groups.all()
                for group in group_iterator:
                    #print(usr.name)
                    groups.append(group.name)
                    worksheet.write(0, Group_Names.index(group.name)+2,group.name)
                    worksheet.write(row, Group_Names.index(group.name)+2,"X")
                if not groups:
                    worksheet.write(row, 1,"No")
                #worksheet.write(row, 3,', '.join(groups))
                
                
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