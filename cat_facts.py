""" HTTP Cat facts delivery from DynamoDB """
import json
import os
import uuid
import boto3
from boto3.dynamodb.conditions import Key

TABLE = boto3.resource('dynamodb').Table(os.environ['TABLE_NAME'])

#def get(event, context):
def get():
    """ Get method returning cat fact. """
    random_uuid = uuid.uuid4()

    try:
        result = TABLE.query(Limit=1, KeyConditionExpression=Key('sortId').gte(str(random_uuid))
                             & Key('id').eq('cat-fact'))

        if result['Items']:
            result = TABLE.query(Limit=1, KeyConditionExpression=Key('sortId').lt(str(random_uuid))
                                 & Key('id').eq('cat-fact'))

        if result['Items']:
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
