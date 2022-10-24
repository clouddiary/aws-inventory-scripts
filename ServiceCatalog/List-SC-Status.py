#
# Script takes input file with Service Catalog launched product name & creates excel inventory with all info.
# AWS CLI profile needs to be created on machine where script will run & pass profile name.

import boto3
import json
import xlsxwriter
import sys


# aws servicecatalog scan-provisioned-products --access-level-filter Key="Account",Value="self"  --query "ProvisionedProducts[*].[Id]" --profile crx-dev-readonly --output text  > PP-List.txt

session = boto3.Session(profile_name='qa')
client = session.client('servicecatalog')

filepath="PP-List.txt"
#
# Create the Spread Sheet containing all information about EC2.
#
# Creating Excel worksheet
workbook = xlsxwriter.Workbook('Provisioned-Product-Status.xlsx')

bold = workbook.add_format({'bold': True})
row = 0
worksheet = workbook.add_worksheet('Provsioned Product')
worksheet.write(row, 0, 'Name', bold)
worksheet.write(row, 1, 'Id', bold)
worksheet.write(row, 2, 'Status', bold)


#paginator = client.get_paginator('list_ProvisionedProductDetail')
#pp_details = client.describe_provisioned_product(Id='pp-4imiktfr63cog')
#print(pp_details['ProvisionedProductDetail']['Name'])


with open(filepath) as fp:
       cnt = 0
       for line in fp:
           Name=line.strip()
           try:
            pp_details = client.describe_provisioned_product(Id=Name)
            row += 1
            #print(pp_details['ProvisionedProductDetail'][0]['Name'],pp_details['ProvisionedProductDetail'][0]['Tags'])
            worksheet.write(row, 0, pp_details['ProvisionedProductDetail']['Name'])
            worksheet.write(row, 1, pp_details['ProvisionedProductDetail']['Id'])
            worksheet.write(row, 2, pp_details['ProvisionedProductDetail']['Status'])
           except:
                 print(Name," is not exist")
                
workbook.close()
print("Inventory is created")