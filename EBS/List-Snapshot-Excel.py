#
# Script pulls all snapshots & dumps info in excel
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
workbook = xlsxwriter.Workbook('EC2-All-Snapshots.xlsx')

#Define bold, so that we can use later
bold = workbook.add_format({'bold': True})

#Formating cells to left
cell_format = workbook.add_format()
cell_format.set_align('left')

#Define first row
row = 0

#Define worksheet name
worksheet = workbook.add_worksheet('Snapshots Info')

#Define Headers for the spreadsheet
worksheet.write(row, 0, 'Snapshot ID', bold)
worksheet.write(row, 1, 'Description', bold)
worksheet.write(row, 2, 'Volume Size', bold)
worksheet.write(row, 3, 'Creation Date', bold)
worksheet.write(row, 4, 'Owner ID', bold)
#worksheet.write(row, 4, 'Associated Instances', bold)

#Increment row, so that results can be written on 2nd row
row += 1

#Initialize ec2 resource
ec2 = session.resource('ec2')

#Getting all snapshots
snapshot_iterator = ec2.snapshots.all()

# Iterating through the snapshots and printing id, description, size and creation date
for snapshot in snapshot_iterator:
    worksheet.write(row, 0, snapshot.id)
    worksheet.write(row, 1, snapshot.description)
    worksheet.write(row, 2, snapshot.volume_size, cell_format)
    worksheet.write(row, 3, snapshot.start_time.strftime("%m/%d/%Y, %H:%M:%S"))
    worksheet.write(row, 4, snapshot.owner_id)
    row += 1

# Closing the speadsheet
workbook.close()
print("Inventory is created")