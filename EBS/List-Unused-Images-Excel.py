#
# Script pulls all AMIS in an aws account along with instance id using same AMI in excel
#
# AWS CLI profile needs to be created on machine where script will run & pass profile name.

import sys
import boto3
from datetime import datetime
import argparse
import xlsxwriter

## Update local aws cli profile name here
session = boto3.Session(profile_name='qa')

#The Excel document name where results will be shared
workbook = xlsxwriter.Workbook('EC2-All-AMIs.xlsx')

#Define bold, so that we can use later
bold = workbook.add_format({'bold': True})

#Define first row
row = 0

#Define worksheet name
worksheet = workbook.add_worksheet('AMIs Info')

#Define Headers for the spreadsheet
worksheet.write(row, 0, 'ImageID', bold)
worksheet.write(row, 1, 'ImageName', bold)
worksheet.write(row, 2, 'ImageStatus', bold)
worksheet.write(row, 3, 'Creation Date', bold)
worksheet.write(row, 4, 'Associated Instances', bold)

#Increment row, so that results can be written on 2nd row
row += 1

#Initialize ec2 resource
ec2 = session.resource('ec2')

#Filtering images to images owned by us only
image_iterator = ec2.images.filter(Owners=[
        'self',
    ])

# Iterating through the images and printing id, name, state and associated instances.
for img in image_iterator:
    instance_list=[]
    print(img.id,img.state)
    instance_iterator = ec2.instances.filter(
        Filters=[
        {
            'Name': 'image-id',
            'Values': [img.id],            
        }
    ])
    for instance in instance_iterator:
        instance_list.append(instance.id)
    worksheet.write(row, 0, img.id)
    worksheet.write(row, 1, img.name)
    worksheet.write(row, 2, img.state)
    worksheet.write(row, 3, img.creation_date)
    worksheet.write(row, 4, ', '.join(instance_list))
    row += 1

# Closing the speadsheet
workbook.close()
print("Inventory is created")