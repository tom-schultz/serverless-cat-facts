import boto3
from boto3.dynamodb.conditions import Key
import json
import os
import uuid

table = boto3.resource('dynamodb').Table(os.environ['TABLE_NAME'])

def get(event, context):
    random_uuid = uuid.uuid4()

    try:
        result = table.query(Limit=1, KeyConditionExpression=Key('sortId').gte(str(random_uuid)) & Key('id').eq('cat-fact'))

        if len(result['Items']) == 0:
            result = table.query(Limit=1, KeyConditionExpression=Key('sortId').lt(str(random_uuid)) & Key('id').eq('cat-fact'))

        if len(result['Items']) == 0:
            raise KeyError
    except KeyError:
        raise Exception('Couldn\'t get a random item.')

    response = {'cat-fact': next(iter(result['Items']))['cat-fact']}

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(response)
    }
