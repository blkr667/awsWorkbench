import boto3
import os

table_name = os.environ['TABLE_NAME']
dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    print('test get')
    table = dynamodb.Table(table_name)

    records = table.scan()

    print(records)
    return records
