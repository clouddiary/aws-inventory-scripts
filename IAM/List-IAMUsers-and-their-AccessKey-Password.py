#
# Script pulls all IAM users having access keys with their password & last activity
#
# AWS CLI profile needs to be created on machine where script will run & pass profile name.

import boto3
import json
import xlsxwriter
import sys
from datetime import datetime
import json

## Update local aws cli profile name here
session = boto3.Session(profile_name='qa')

lam = session.client('iam')
iam = session.resource('iam')


Next_Token = None

###############################
### Create the Spread Sheet ###
###############################
workbook = xlsxwriter.Workbook('List-IAMUser-WithccessKeys-Password.xlsx')
date_format = workbook.add_format({'num_format': 'd mmm yyyy'})
bold = workbook.add_format({'bold': True})
row = 0
flag = 0
SheetName = 'EC2 Instances'
worksheet = workbook.add_worksheet('IAMUser')
worksheet.write(row, 0, 'User Name', bold)
worksheet.write(row, 1, 'Arn', bold)
worksheet.write(row, 2, 'Password', bold)
worksheet.write(row, 3, 'AccessKey', bold)
worksheet.write(row, 4, 'LastUsed', bold)
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
            worksheet.write(row, 0, user['UserName'])
            try:                
                #worksheet.write(row, 1,user['UserId'])
                #worksheet.write(row, 2,user['Arn'])
                user2 = iam.User(user['UserName'])
                #worksheet.write(row, 1, user2.user_id)
                worksheet.write(row, 1, user2.arn)
                if user2.password_last_used is None:
                    worksheet.write(row, 2, "No Password")
                else:
                    worksheet.write(row, 2, user2.password_last_used.strftime("%m/%d/%Y, %H:%M:%S"))
                access_key_iterator = user2.access_keys.all()
                #print(len(access_key_iterator))
                flag = 0 
                for i in access_key_iterator:
                    if i.user_name == user['UserName']:
                        #print(i.user_name)
                        #worksheet.write(row, 3, "Enabled")
                        response = lam.get_access_key_last_used(AccessKeyId=i.id)
                        worksheet.write(row, 3, i.id)
                        worksheet.write(row, 4, response['AccessKeyLastUsed']['LastUsedDate'].strftime("%m/%d/%Y, %H:%M:%S"))
                        row += 1
                        flag = 1
                        #print(response['AccessKeyLastUsed']['LastUsedDate'])
                    else:
                        worksheet.write(row, 3, "None")
                
            except KeyError:
                print()
                #worksheet.write(row, 1,"")
            if flag == 1:
               row -= 1
               
            row += 1

    try:
        Next_Token = page['nextToken']
        print(Next_Token)
    except KeyError:
    #    sys.exit()
        break


workbook.close()
print("Inventory is created")