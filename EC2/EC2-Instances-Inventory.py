#
# Script Creates Spread Sheet containing all information about EC2 instances running in a specific AWS account.
#
# AWS CLI profile needs to be created on machine where script will run & pass profile name on line 14.

import boto3
import json
import xlsxwriter
from datetime import datetime


## Modify profile name, environment  name & excel file name before you run this script
## profile_name would be local aws cli profile
session = boto3.Session(profile_name='qa')
ec2 = session.resource('ec2')

env = "QA"
now = datetime.now()
date_time = now.strftime("%m-%d-%Y")
filename = "EC2-Instances-"+env +"-"+date_time +".xlsx" 
workbook = xlsxwriter.Workbook(filename)

bold = workbook.add_format({'bold': True})


row = 0

#Defining Worksheet and its fields.
worksheet = workbook.add_worksheet('EC2 Instances')
worksheet.write(row, 0, 'InstanceName', bold)
worksheet.write(row, 1, 'InstanceId', bold)
worksheet.write(row, 2, 'State', bold)
worksheet.write(row, 3, 'ASG', bold)
worksheet.write(row, 4, 'PrivateIP', bold)
worksheet.write(row, 5, 'PublicIP', bold)
worksheet.write(row, 6, 'Type', bold)
worksheet.write(row, 7, 'Platform', bold)
worksheet.write(row, 8, 'ImageID', bold)
worksheet.write(row, 9, 'System', bold)
worksheet.write(row, 10, 'SubSystem', bold)
worksheet.write(row, 11, 'Environment', bold)

row += 1

#Use below to filter to Running states only.
#all_instances = ec2.instances.filter(Filters=[{
#    'Name': 'instance-state-name',
#    'Values': ['running']}])

all_instances = ec2.instances.filter()

#Iterate through instances and print required stats.
for instance in all_instances:
    worksheet.write(row, 1, instance.id)
    worksheet.write(row, 2, instance.state['Name'])
    #worksheet.write(row, 3, instance.asg)
    worksheet.write(row, 4, instance.private_ip_address)
    worksheet.write(row, 5, instance.public_ip_address)
    worksheet.write(row, 6, instance.instance_type)
    worksheet.write(row, 7, instance.platform)
    worksheet.write(row, 8, instance.image_id)
    
#Special handling of tags (name and autoscaling group name), you can add/remove/modify based on your environment/tags
    try:
        for tag in instance.tags:
            if 'Name'in tag['Key']:
                if tag['Key'] == "Name" :
                    name = tag['Value']
                    worksheet.write(row, 0, name, bold)
            if 'aws:autoscaling:groupName'in tag['Key']:
                worksheet.write(row, 3, tag['Value'])
            if 'System' in tag['Key']:
                if tag['Key'] == "System" :
                    worksheet.write(row, 9, tag['Value'])
            if 'SubSystem' in tag['Key']:
                if tag['Key'] == "SubSystem" :
                 worksheet.write(row, 10, tag['Value'])
            if 'Environment' in tag['Key']:
                worksheet.write(row, 11, tag['Value'])

               
               
    except TypeError:
        worksheet.write(row, 0, "")
        
    row += 1

# Closing the Excel.
workbook.close()
print("Inventory is created")