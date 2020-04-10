import boto3
import json
import os

table_name = os.environ['TABLE_NAME']
dynamodb_client = boto3.client('dynamodb')


def lambda_handler(event, context):
	return "kruci bomba"
	print("This line will be printed.")
	print(event['body'])
	body = json.loads(event['body'])
	print(body)
	print(body['distance'])
	print(body['date'])

	try:
		response = dynamodb_client.describe_table(TableName='table_name')
		print("table test exists")



		dynamodb_client.put_item(TableName='blazej-stack2-myDynamoDBTable-1HXG0GR86FVBZ', Item={
			'date': {'S': body['date']},
			'distance': {'N': str(body['distance'])},
			'blazejkey': {'S': body['date']}
		})


		return "hakimbo"
	except dynamodb_client.exceptions.ResourceNotFoundException:
		print("table test not exists")
		return "makumbo"
	return "kojumbo"

