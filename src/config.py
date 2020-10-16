import os
import boto3

ssm = boto3.client('ssm')

if os.environ.get('SSM_SLACK_WEBHOOK_URL'):
    SLACK_WEBHOOK_URL = ssm.get_parameter(Name=os.environ['SSM_SLACK_WEBHOOK_URL'],
                                          WithDecryption=True)['Parameter']['Value']
else:
    SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']

if os.environ.get('SSM_KIBELA_API_TOKEN'):
    KIBELA_API_TOKEN = ssm.get_parameter(Name=os.environ['SSM_KIBELA_API_TOKEN'],
                                         WithDecryption=True)['Parameter']['Value']
else:
    KIBELA_API_TOKEN = os.environ.get('KIBELA_API_TOKEN')

KIBELA_BASE_URL = os.environ.get('KIBELA_BASE_URL')
