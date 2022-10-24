#
# Script pulls all IAM users of IAM group
#
# AWS CLI profile needs to be created on machine where script will run & pass profile name.

import boto3
import json
import xlsxwriter
import sys

## Update local aws cli profile name here
session = boto3.Session(profile_name='qa')
iam = session.resource('iam')
users=[]
group = iam.Group('AWS-Admins')
user_iterator = group.users.all()
for usr in user_iterator:
    print(usr.name)
    users.append(usr.name)


print(users)
print(user_iterator)