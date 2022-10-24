#
# Script pulls EC2 instance & check EBS volume ecryption status for each volume attached to each EC2 instance.
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
#instance_iterator = ec2.instances.all()

# Update VPC ID
vpc = ec2.Vpc('vpc-id-12345')
instance_iterator = vpc.instances.all()

for it in instance_iterator:
    #print(it.id)
    volumes = it.volumes.all()
    for v in volumes:
       # if v.encrypted:
                try:
                    for tag in it.tags:
                        if tag['Key'] == 'Name':
                            print(tag['Value'],"#",it.id,"#",v.id,"#",v.encrypted,"#",v.kms_key_id,"#",it.state)
                except:
                    print("None","#",it.id,"#",v.id,"#",v.encrypted,"#",v.kms_key_id,"#",it.state)                