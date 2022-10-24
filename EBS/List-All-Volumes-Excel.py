#
# Script pulls all volumens in an aws account along with its status, type & size
#
# AWS CLI profile needs to be created on machine where script will run & pass profile name.

import sys
import boto3
from datetime import datetime
import argparse
import xlsxwriter

## Update local aws cli profile name here
session = boto3.Session(profile_name='qa')

ec2 = session.resource('ec2')

#
# Create the Spread Sheet for volume results.
#
workbook = xlsxwriter.Workbook('List-Volumes.xlsx')
bold = workbook.add_format({'bold': True})
row = 0
SheetName = 'EC2 Instances'
worksheet = workbook.add_worksheet('Volumes')
worksheet.write(row, 0, 'VolumeID', bold)
worksheet.write(row, 1, 'VolumeState', bold)
worksheet.write(row, 2, 'SnapshotID', bold)
worksheet.write(row, 3, 'VolumeType', bold)
worksheet.write(row, 4, 'VolumeSize', bold)
row += 1

#Iterating through volumes and printing detatils.

volume_iterator = ec2.volumes.all()
for vol in volume_iterator:
    #print(vol.id,vol.state,vol.snapshot_id,vol.volume_type, vol.size)
    worksheet.write(row, 0, vol.id)
    worksheet.write(row, 1, vol.state)
    worksheet.write(row, 2, vol.snapshot_id)
    worksheet.write(row, 3, vol.volume_type)
    worksheet.write(row, 4, vol.size)
    row += 1

#Closing the workbook after printing the results.
workbook.close()
print("Inventory is created")
