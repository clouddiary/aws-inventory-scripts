#
# Script pulls ALBs & finds out incoming traffic rules on attached SG.
#
# AWS CLI profile needs to be created on machine where script will run & pass profile name.

## Update local aws cli profile name here

import boto3
import json
import xlsxwriter
import sys

# Function to convert  
def listToString(s): 
    #print(s)
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += ele['CidrIp']
        str1 += ","  
    
    # return string  
    return str1

security_group_id_col = 6
security_group_id_name = 7
direction_col = 8
protocol_col = 9
from_col = 10
to_col = 11
ip_col = 12
vpc_col = 13 

session = boto3.Session(profile_name='qa')
alb = session.client('elbv2')
ec2 = session.resource('ec2')


Next_Token = None

#
# Create the Spread Sheet
#
workbook = xlsxwriter.Workbook('tezs-qa-ALBs.xlsx')
bold = workbook.add_format({'bold': True})
row = 0
SheetName = 'ALB Info'
worksheet = workbook.add_worksheet('ALBs')
worksheet.write(row, 0, 'LB Name', bold)
worksheet.write(row, 1, 'DNSName', bold)
worksheet.write(row, 2, 'LoadBalancerArn', bold)
worksheet.write(row, 3, 'Type', bold)
worksheet.write(row, 4, 'VPCID', bold)
worksheet.write(row, 5, 'SecurityGroup', bold)


row += 1

while True:
    
    paginator = alb.get_paginator('describe_load_balancers')
    print("HelloOOOOOOOOOOOOOOOOOOO: ",Next_Token)
    response_iterator = paginator.paginate(
        PaginationConfig={
                'MaxItems': 300,
                'PageSize': 100,
                'StartingToken': Next_Token}
    )

    for page in response_iterator:
        lbs = page['LoadBalancers']
        
        
        for lb in lbs:
            
            worksheet.write(row, 0, lb['LoadBalancerName'])
            try:
                print(lb['DNSName'])
                worksheet.write(row, 1,lb['DNSName'])
                worksheet.write(row, 2,lb['LoadBalancerArn'])
                worksheet.write(row, 3,lb['Scheme'])
                worksheet.write(row, 4,lb['VpcId'])
                #worksheet.write(row, 5,' '.join(lb['SecurityGroups']))
                
                for security_group in lb['SecurityGroups']:
                    sg = ec2.SecurityGroup(security_group)
                    for x in sg.ip_permissions:
                        try:
                            if x['IpProtocol'] == '-1':
                                worksheet.write(row, 0, lb['LoadBalancerName'])
                                worksheet.write(row, 1, lb['DNSName'])
                                worksheet.write(row, 2, lb['LoadBalancerArn'])
                                worksheet.write(row, 3, lb['Scheme'])
                                worksheet.write(row, 4, lb['VpcId'])
                                worksheet.write(row, 5,' '.join(lb['SecurityGroups']))
                                worksheet.write(row, security_group_id_col , security_group)
                                worksheet.write(row, direction_col, 'Inbound')
                                worksheet.write(row, protocol_col, x['IpProtocol'])                    
                                worksheet.write(row, ip_col, listToString(x['IpRanges']))
                                row += 1
                            else:
                                worksheet.write(row, 0, lb['LoadBalancerName'])
                                worksheet.write(row, 1, lb['DNSName'])
                                worksheet.write(row, 2, lb['LoadBalancerArn'])
                                worksheet.write(row, 3, lb['Scheme'])
                                worksheet.write(row, 4, lb['VpcId'])
                                worksheet.write(row, 5,' '.join(lb['SecurityGroups']))
                                worksheet.write(row, security_group_id_col, security_group)
                                worksheet.write(row, direction_col, 'Inbound')
                                worksheet.write(row, protocol_col, x['IpProtocol'])
                                worksheet.write(row, from_col, x['FromPort'])
                                worksheet.write(row, to_col, x['ToPort'])
                                worksheet.write(row, ip_col, listToString(x['IpRanges']))
                                row += 1   
                                          
                        except KeyError as k:
                            print ('Error --> ', k)
                            print ('SG: ', security_group)
                            print (json.dumps(sg.ip_permissions))
                            print ('')
                            continue
                
            except KeyError as Er:
                print('Error --> ', Er)
                worksheet.write(row, 1,"")
            row += 1
        
    try:
        Next_Token = page['nextToken']
        print(Next_Token)
    except KeyError:
    #    sys.exit()
        break


workbook.close()
print("Inventory is created")