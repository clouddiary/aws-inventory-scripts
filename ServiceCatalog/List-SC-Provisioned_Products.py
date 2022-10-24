
#
# Script pulls list of self launched Service Catalog products
# AWS CLI profile needs to be created on machine where script will run & pass profile name.

#aws servicecatalog scan-provisioned-products --access-level-filter Key="Account",Value="self"  --query "ProvisionedProducts[*].[Name,Id,ProductId]" --profile crx-dev-readonly --output text  > SC-List.txt

import boto3
import json
import xlsxwriter

session = boto3.Session(profile_name='qa')
client = session.client('servicecatalog')

all_provisoned_products = client.scan_provisioned_products(
    AccessLevelFilter={
        'Key': 'User',
        'Value': 'self'
    },
   
)

for product in all_provisoned_products['ProvisionedProducts']:
    print("Hello")
    print(product['Name'], product['Id'],product['ProductId'])
