#
# Script scan all EC2 instances for their attached roles & checks if AmazonSSMManagedInstanceCore policy is attached in role
#
# AWS CLI profile needs to be created on machine where script will run & pass profile name.

import boto3
import json
import xlsxwriter
from botocore.exceptions import ClientError

profile_name='qa'
session = boto3.Session(profile_name=profile_name)
ec2 = session.resource('ec2')
client = session.client('iam')


all_instances = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running']}])

for instance in all_instances:
    isRole_good = 0
    #print(instance.id,instance.iam_instance_profile['Arn'] )
    role = instance.iam_instance_profile['Arn'].split("/",1)[1]
    try:
        role_response = client.list_attached_role_policies(RoleName=role)
        #print(role_response)
        for policy in role_response['AttachedPolicies']:
            if policy['PolicyName'] == "AmazonSSMManagedInstanceCore":
                isRole_good += 1
        if (isRole_good != 1):
            print (instance.id, role, "fix it")
    except ClientError:
        print(instance.id, role,"check/fix it")

