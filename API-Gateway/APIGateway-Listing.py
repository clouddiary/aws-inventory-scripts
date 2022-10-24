#
# Script checks specific tags in  API gateway stage & prints missing one
#
# AWS CLI profile needs to be created on machine where script will run & pass profile name.

import boto3
import json
from botocore.exceptions import ClientError

profile_name='qa'
session = boto3.Session(profile_name=profile_name)
client = session.client('apigateway')
Next_Token = None



resourceArn='arn:aws:apigateway:us-east-1::/restapis/lbd1kquyge/stages/qa'
current_tags=[]
try:
    stage = client.get_tags(resourceArn=resourceArn)
    print("STAGE:",stage)
    print("STAGE TAGS:",stage["tags"])
    if stage["tags"]:
        for x in stage["tags"]:
            current_tags.append(x)
        if 'API-AccessLogging' not in current_tags or 'API-Xray' not in current_tags :
            compliance_type = 'NON_COMPLIANT'
            annotation = "API stage does NOT have one or both tags, " \
                + "API-AccessLogging and API-Xray"
        else:
            compliance_type = 'COMPLIANT'
            annotation = 'API stage has the tags.'
except:
    compliance_type = 'NON_COMPLIANT'
    annotation = 'API stage missing the tags..'
print(compliance_type,":",annotation)

#response = client.get_tags(resourceArn='arn:aws:apigateway:us-east-1::/restapis/lbd1kquyge/stages/qa')
#print(response)
#print(response['tags'])
'''

r = 1
while True:

    paginator = client.get_paginator('get_rest_apis')

    response_iterator = paginator.paginate(
        PaginationConfig={
            'MaxItems': 300,
            'PageSize': 100,
            'StartingToken': Next_Token
        }
    )
    for page in response_iterator:
            items = page['items']
            for item in items:
                print(r,":",item['id'],item['name'])
                stages = client.get_stages(restApiId=item['id'])
                try:
                    print(stages['item'][0]['deploymentId'],stages['item'][0]['stageName'])
                    tags = stages['item'][0]['tags']
                    print ("tags:", tags)
                    current_tags=[]
                    
                    for x in tags:
                        current_tags.append(x)
                    if 'API-AccessLogging' not in current_tags or 'API-Xray' not in current_tags :
                        print("INFO:NON-COMPLAINT")
                    else:
                        print("INFO:COMPLAINT")
                        
                except IndexError as i:
                    print(i)
                except KeyError as k:
                    print(k)
                    print("INFO:NON-COMPLAINT")

                
                #print(stages)
                r += 1


    try:
        Next_Token = page['nextToken']
        print(Next_Token)
    except KeyError:
        #    sys.exit()
        break
'''