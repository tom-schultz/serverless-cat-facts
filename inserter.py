import boto3
import uuid
import urllib2
import json

def main():
    table = boto3.resource('dynamodb').Table('CatFacts')
    url = urllib2.urlopen("https://raw.githubusercontent.com/vadimdemedes/cat-facts/master/cat-facts.json")
    raw = url.read()
    url.close()
    parsed = json.loads('{"facts": ' + raw + "}")

    for fact in parsed['facts']:
        sort_id = str(uuid.uuid4())
        table.put_item(Item={'id': 'cat-fact', 'sortId': sort_id, 'cat-fact': fact}, )

if __name__ == '__main__':
    main()
