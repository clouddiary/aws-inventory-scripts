#
# Script pulls EC2 instance with VPC ID, SG, Incoming, Outgoing port info & dumps in excel
#
# AWS CLI profile needs to be created on machine where script will run & pass profile name.

import boto3
import json
import xlsxwriter

# Function to convert  
def listToString(s): 
    print(s)
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += ele['CidrIp']
        str1 += ","  
    
    # return string  
    return str1 

## Update local aws cli profile name here
session = boto3.Session(profile_name='qa')
client = session.client('ec2')

response = client.describe_instances()

workbook = xlsxwriter.Workbook('EC2 - Security Groups, Ports, and Protocols.xlsx')
bold = workbook.add_format({'bold': True})
worksheet = workbook.add_worksheet("SecurityGroups")

row = 0
direction_col = 4
protocol_col = 5
from_col = 6
to_col = 7
ip_col = 8
vpc_col = 9
worksheet.write(row, 0, 'Instance:', bold)
worksheet.write(row, 1, 'Instance ID:', bold)
worksheet.write(row, 2, 'SG ID:', bold)
worksheet.write(row, 3, 'SG Name:', bold)
worksheet.write(row, direction_col, 'Direction', bold)
worksheet.write(row, protocol_col, 'Protocl', bold)
worksheet.write(row, from_col, 'From Port', bold)
worksheet.write(row, to_col, 'To Port', bold)
worksheet.write(row, ip_col, 'CidrIp', bold)
worksheet.write(row, vpc_col, 'VPC', bold)

row += 1

for r in response['Reservations']:
    for i in r['Instances']:
        
        InstanceName = ''
        for t in i['Tags']:
            if t['Key'] == 'Name':
                InstanceName =  t.get('Value')

        for security_group in i['SecurityGroups']:
            
            

            protocol = ''
            from_port = ''
            to_port = ''
            ec2 = session.resource('ec2')
            sg = ec2.SecurityGroup(security_group['GroupId'])
            for x in sg.ip_permissions:
                try:
                    if x['IpProtocol'] == '-1':
                        worksheet.write(row, 0, InstanceName)
                        worksheet.write(row, 1, i['InstanceId'])
                        worksheet.write (row, 2, security_group['GroupId'])
                        worksheet.write (row, 3, security_group['GroupName'])
                        worksheet.write(row, direction_col, 'Inbound')
                        worksheet.write(row, protocol_col, 'All')
                        worksheet.write(row, protocol_col, 'All')
                        worksheet.write(row, vpc_col, i['NetworkInterfaces'][0]['VpcId'])
                        #print("Hello $$$$$$$$$$$$$$$$$$$",i['NetworkInterfaces'][0]['VpcId'])                        
                        worksheet.write(row, ip_col, listToString(x['IpRanges']))
                        #worksheet.write(row, vpc_col, i['IpRanges']['NetworkInterfaces']['VpcId'])
                        
                        #worksheet.write(row, protocol_col, x['IpProtocol'])
                        row += 1
                    else:
                        worksheet.write(row, 0, InstanceName)
                        worksheet.write(row, 1, i['InstanceId'])
                        worksheet.write (row, 2, security_group['GroupId'])
                        worksheet.write (row, 3, security_group['GroupName'])
                        worksheet.write(row, direction_col, 'Inbound')
                        worksheet.write(row, protocol_col, x['IpProtocol'])
                        worksheet.write(row, from_col, x['FromPort'])
                        worksheet.write(row, to_col, x['ToPort'])
                        worksheet.write(row, vpc_col, i['NetworkInterfaces'][0]['VpcId'])
                        #print("Hello $$$$$$$$$$$$$$$$$$$",i['NetworkInterfaces'][0]['VpcId']) 
                        worksheet.write(row, ip_col, listToString(x['IpRanges']))
                        #worksheet.write(row, vpc_col, i['IpRanges']['NetworkInterfaces']['VpcId'])
                        
                        row += 1
                    
                except KeyError as k:
                    print ('Error --> ', k)
                    print ('SG: ', security_group['GroupName'])
                    print (json.dumps(sg.ip_permissions))
                    print ('')
                    continue

            for x in sg.ip_permissions_egress:
                try:
                    if x['IpProtocol'] == '-1':
                        worksheet.write(row, 0, InstanceName)
                        worksheet.write(row, 1, i['InstanceId'])
                        worksheet.write (row, 2, security_group['GroupId'])
                        worksheet.write (row, 3, security_group['GroupName'])
                        worksheet.write(row, direction_col, 'Outbound')
                        worksheet.write(row, protocol_col, x['IpProtocol'])
                        worksheet.write(row, to_col + 1, listToString(x['IpRanges']))
                        worksheet.write(row, vpc_col, i['NetworkInterfaces'][0]['VpcId'])
                        row += 1
                    else:
                        worksheet.write(row, 0, InstanceName)
                        worksheet.write(row, 1, i['InstanceId'])
                        worksheet.write (row, 2, security_group['GroupId'])
                        worksheet.write (row, 3, security_group['GroupName'])
                        worksheet.write(row, direction_col, 'Outbound')
                        worksheet.write(row, protocol_col, x['IpProtocol'])
                        worksheet.write(row, from_col, x['FromPort'])
                        worksheet.write(row, to_col, x['ToPort'])
                        worksheet.write(row, to_col + 1, listToString(x['IpRanges']))
                        worksheet.write(row, vpc_col, i['NetworkInterfaces'][0]['VpcId'])
                        row += 1
                except KeyError as k:
                    print ('Error --> ', k)
                    print ('SG: ', security_group['GroupName'])
                    print (json.dumps(sg.ip_permissions))
                    print ('')
                    continue
            #row +=1

workbook.close()
