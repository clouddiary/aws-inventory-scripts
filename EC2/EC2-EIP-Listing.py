#
# Script pulls list of EIP & dumps associated instancesid & private ip in excel sheet.
#
# AWS CLI profile needs to be created on machine where script will run & pass profile name.

import boto3
import json
import xlsxwriter
import sys

## Update local aws cli profile name here
session = boto3.Session(profile_name='qa')
#ec2 = session.resource('ec2')
client = session.client('ec2')


workbook = xlsxwriter.Workbook('tezs-qa-eip-inventory.xlsx')
bold = workbook.add_format({'bold': True})
row = 0
SheetName = 'EIP Info'
worksheet = workbook.add_worksheet('EIP')
worksheet.write(row, 0, 'PublicIp', bold)
worksheet.write(row, 1, 'InstanceId', bold)
worksheet.write(row, 2, 'PrivateIpAddress', bold)


row += 1


addresses_dict = client.describe_addresses()
for eip_dict in addresses_dict['Addresses']:
    #print(row," : ",eip_dict['PublicIp']," ", eip_dict['InstanceId']," ", eip_dict['PrivateIpAddress'])
    worksheet.write(row, 0, eip_dict['PublicIp'])
    try:
        worksheet.write(row, 1, eip_dict['InstanceId'])
    except:
        worksheet.write(row, 1, "")
    
    try:
        worksheet.write(row, 2, eip_dict['PrivateIpAddress'])
    except:
        worksheet.write(row, 2, "")
    
    
    row += 1

workbook.close()
print("Inventory is created")