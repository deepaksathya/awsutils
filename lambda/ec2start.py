# this Code will help to schedule stop the EC2 using Lambda
# Yesh
# Version -- 2.0

import boto3
import os
import sys
import time
from datetime import datetime, timezone
from time import gmtime, strftime


def shut_ec2_all():
    region = os.environ['REGION']
    key = os.environ['KEY']
    value = os.environ['VALUE']

    client = boto3.client('ec2', region_name=region)
    response = client.describe_instances()
    # print(response)
    for group in response['Reservations']:
        for i in group['Instances']:
            # ec2instance=i['InstanceId']
            tags = i['Tags']
            for tag in tags:
                # If the tags match, then stop the instances by validating the current status.
                if tag['Key'] == key and tag['Value'] == value:
                    if i['State']['Name'] == 'stopped':
                        instances = [i['InstanceId']]
                        client.start_instances(InstanceIds=instances)
                        print('stopping EC2 instance {0}'.format(
                            i['InstanceId']))
                    elif i['State']['Name'] == 'running':
                        print('EC2 Instance {0} is already in running state'.format(
                            i['InstanceId']))
                    elif i['State']['Name'] == 'pending':
                        print('EC2 Instance {0} is in pending state. Please stop the server after starting is complete'.format(
                            i['EC2InstanceIdentifier']))
                    elif i['State']['Name'] == 'stopping':
                        print('EC2 Instance {0} is in stopping state.  Please wait before starting'.format(
                            i['InstanceId']))
                    elif tag['Key'] != key and tag['Value'] != value:
                        print('EC2 instance {0} is not part of auto start'.format(
                            i['InstanceId']))


def lambda_handler(event, context):
    shut_ec2_all()
