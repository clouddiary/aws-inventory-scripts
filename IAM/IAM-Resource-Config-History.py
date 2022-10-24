# Ensure that no users have been inactive for a period longer than specified.
# Description: Checks that all users have been active for earlier than specified.
#
# Trigger Type: Change Triggered
# Scope of Changes: IAM:User
# Required Parameters: maxInactiveDays
# Example Value: 90
# Example $: python.exe .\Resource-Config-History.py -n "90"
import json
import boto3
import datetime
import argparse

APPLICABLE_RESOURCES = ["AWS::IAM::User"]
session = boto3.Session(profile_name='qa')

def calculate_age(date):
    now = datetime.datetime.utcnow().date()
    then = date.date()
    age = now - then
    print(age.days)
    return age.days
def evaluate_compliance(configuration_item, rule_parameters):
    if configuration_item["resourceType"] not in APPLICABLE_RESOURCES:
        return "NOT_APPLICABLE"
    config = session.client("config")
    resource_information = config.get_resource_config_history(
        resourceType=configuration_item["resourceType"],
        resourceId=configuration_item["resourceId"]
    )
    user_name = resource_information["configurationItems"][0]["resourceName"]
    print("User Name: ",user_name)
    iam = session.client("iam")
    user = iam.get_user(UserName=user_name)
    last_used = user["User"].get("PasswordLastUsed")
    print("Last used: ",last_used)
    max_inactive_days = int(rule_parameters["maxInactiveDays"])
    if last_used is not None and calculate_age(last_used) > max_inactive_days:
        print("NON_COMPLIANT")
        return "NON_COMPLIANT"
    print("COMPLIANT")
    return "COMPLIANT"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-n',
        '--max_days',
        type=str,
        required=True,
        help="Number of days back")
    
    args = parser.parse_args()
    print(args.max_days)
    #evaluate_compliance({"resourceType":"AWS::IAM::User","resourceId":"AIDAJB5B3FCOD3LNGMU6S"},{"maxInactiveDays":args.max_days})
    evaluate_compliance({"resourceType":"AWS::IAM::User","resourceId":"AIDAIR5YSQ755MMUOOAPK"},{"maxInactiveDays":args.max_days})   