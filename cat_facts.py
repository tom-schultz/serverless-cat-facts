import boto3
import json
import os

table = boto3.resource('dynamodb').Table(os.environ['TABLE_NAME'])

def get(event, context):
    try:
        result = table.scan(ExclusiveStartKey={'id': '00000'}, Limit=1)

        if len(result['Items']) == 0:
            raise KeyError
    except KeyError:
        raise Exception('Couldn\'t get a random item.')

    response = {'data': {'cat-fact': result[0]['cat-fact']}}

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(response)
    }
