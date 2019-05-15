from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    response = read_data_all(event)
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
    
def insert_data():
    table = dynamodb.Table('employee')
    record = {}
    record['username']='bobby5'
    record['lastname']='mathew5'
    table.put_item(
        Item={
            'username': record['username'],
            'lastname': record['lastname']
        }
    )
    return 50*50

def read_data_primary():
    table = dynamodb.Table('employee')
    response = table.get_item(
        Key={
            'username': 'bobby'
        }
    )
    return response

def read_data_all(event):
    table = dynamodb.Table('employee')
    filter_key = 'lastname'
    try:
        filter_value = event["queryStringParameters"]['name']
    except Exception as e:
        return {
            'statusCode': 400,
            'body': 'invalid parameter'
    }

    if filter_key and filter_value:
        filtering_exp = Key(filter_key).eq(filter_value)
        response = table.scan(FilterExpression=filtering_exp)
    else:
        response = table.scan()
    
    return response['Items']
