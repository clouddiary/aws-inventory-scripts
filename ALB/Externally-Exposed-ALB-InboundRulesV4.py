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

security_group_id_col = 7
direction_col = 8
protocol_col = 9
from_col = 10
ip_col = 11

session = boto3.Session(profile_name='qa')
alb = session.client('elbv2')
ec2 = session.resource('ec2')


Next_Token = None

#
# Create the Spread Sheet
#
workbook = xlsxwriter.Workbook('tezs-QA-ALBs.xlsx')
bold = workbook.add_format({'bold': True})
row = 0
SheetName = 'ALB Info'
worksheet = workbook.add_worksheet('ALBs')
worksheet.write(row, 0, 'LB Name', bold)
worksheet.write(row, 1, 'DNSName', bold)
worksheet.write(row, 2, 'LoadBalancerArn', bold)
worksheet.write(row, 3, 'Type', bold)
worksheet.write(row, 4, 'Schema', bold)
worksheet.write(row, 5, 'VPCID', bold)
worksheet.write(row, 6, 'SecurityGroups', bold)
worksheet.write(row, 7, 'SecurityGroup', bold)
worksheet.write(row, 8, 'Direction', bold)
worksheet.write(row, 9, 'Protocol', bold)
worksheet.write(row, 10, 'Port', bold)
worksheet.write(row, 11, 'IPs', bold)




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
            
            #worksheet.write(row, 0, lb['LoadBalancerName'])
            try:
                print(lb['DNSName'])
                worksheet.write(row, 0, lb['LoadBalancerName'])
                worksheet.write(row, 1, lb['DNSName'])
                worksheet.write(row, 2, lb['LoadBalancerArn'])
                worksheet.write(row, 3, lb['Type'])
                worksheet.write(row, 4, lb['Scheme'])
                worksheet.write(row, 5, lb['VpcId'])
                
                for security_group in lb['SecurityGroups']:
                    sg = ec2.SecurityGroup(security_group)
                    for x in sg.ip_permissions:
                        #print(x['IpRanges'])
                        try:
                            if '0.0.0.0/0' in listToString(x['IpRanges']):
                                worksheet.write(row, 0, lb['LoadBalancerName'])
                                worksheet.write(row, 1, lb['DNSName'])
                                worksheet.write(row, 2, lb['LoadBalancerArn'])
                                worksheet.write(row, 3, lb['Type'])
                                worksheet.write(row, 4, lb['Scheme'])
                                worksheet.write(row, 5, lb['VpcId'])
                                worksheet.write(row, 6,' '.join(lb['SecurityGroups']))
                                worksheet.write(row, security_group_id_col , security_group)
                                worksheet.write(row, direction_col, 'Inbound')
                                worksheet.write(row, protocol_col, x['IpProtocol'])
                                try:
                                    worksheet.write(row, from_col, x['FromPort'])
                                except KeyError:
                                    worksheet.write(row, from_col, 'All')                    
                                worksheet.write(row, ip_col, listToString(x['IpRanges']))
                                row += 1                             
                                          
                        except KeyError as k:
                            print ('Error inner--> ', k)
                            print ('SG: ', security_group)
                            print (json.dumps(sg.ip_permissions))
                            print ('')
                            continue
                
            except KeyError as Er:
                print('Error outer --> ', Er)
                row += 1
                #worksheet.write(row, 1,"")
                #row += 1
            #row += 1
        
    try:
        Next_Token = page['nextToken']
        print(Next_Token)
    except KeyError:
    #    sys.exit()
        break


nlb = session.client('elb')
Next_Token = None

while True:
    
    paginator = nlb.get_paginator('describe_load_balancers')
    print("HelloOOOOOOOOOOOOOOOOOOO from NLB: ",Next_Token)
    response_iterator = paginator.paginate(
        PaginationConfig={
                'MaxItems': 300,
                'PageSize': 100,
                'StartingToken': Next_Token}
    )

    for page in response_iterator:
        lbs = page['LoadBalancerDescriptions']
        
        
        for lb in lbs:
            
            worksheet.write(row, 0, lb['LoadBalancerName'])
            try:
                print(lb['DNSName'])
                worksheet.write(row, 0, lb['LoadBalancerName'])
                worksheet.write(row, 1, lb['DNSName'])
                #worksheet.write(row, 2, lb['LoadBalancerArn'])
                worksheet.write(row, 3, 'classic')
                worksheet.write(row, 4, lb['Scheme'])
                worksheet.write(row, 5, lb['VPCId'])

                for security_group in lb['SecurityGroups']:
                    sg = ec2.SecurityGroup(security_group)
                    for x in sg.ip_permissions:
                        #print(x['IpRanges'])
                        try:
                            if '0.0.0.0/0' in listToString(x['IpRanges']):
                                worksheet.write(row, 0, lb['LoadBalancerName'])
                                worksheet.write(row, 1, lb['DNSName'])
                                #worksheet.write(row, 2, lb['LoadBalancerArn'])
                                worksheet.write(row, 3, 'classic')
                                worksheet.write(row, 4, lb['Scheme'])
                                worksheet.write(row, 5, lb['VPCId'])
                                worksheet.write(row, 6,' '.join(lb['SecurityGroups']))
                                worksheet.write(row, security_group_id_col , security_group)
                                worksheet.write(row, direction_col, 'Inbound')
                                worksheet.write(row, protocol_col, x['IpProtocol'])
                                try:
                                    worksheet.write(row, from_col, x['FromPort'])
                                except KeyError:
                                    worksheet.write(row, from_col, 'All')                    
                                worksheet.write(row, ip_col, listToString(x['IpRanges']))
                                row += 1                             
                                          
                        except KeyError as k:
                            print ('Error inner--> ', k)
                            print ('SG: ', security_group)
                            print (json.dumps(sg.ip_permissions))
                            print ('')
                            continue

            except KeyError:
                print()
                worksheet.write(row, 1,"")
            #row += 1
        
    try:
        Next_Token = page['nextToken']
        print(Next_Token)
    except KeyError:
    #    sys.exit()
        break


workbook.close()
print("Inventory is created")