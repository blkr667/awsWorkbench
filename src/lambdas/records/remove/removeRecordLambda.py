import boto3
import os

table_name = os.environ['TABLE_NAME']
dynamodb_client = boto3.client('dynamodb')


def lambda_handler(event, context):
	print("This line will be printed.")

	date = ""

	try:
		response = dynamodb_client.describe_table(TableName=table_name)
		print("table test exists")


		dynamodb_client.delete_item(
			TableName='blazej-stack2-myDynamoDBTable-1HXG0GR86FVBZ',
			Key={
				'date': date,
			}
		)

		return "hakimbo"
	except dynamodb_client.exceptions.ResourceNotFoundException:
		print("table test not exists")
		return "makumbo"
	return "kojumbo"

