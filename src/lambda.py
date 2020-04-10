import boto3

dynamodb_client = boto3.client('dynamodb')


def lambda_handler(event, context):
	print("This line will be printed.")
	try:
		response = dynamodb_client.describe_table(TableName='myDynamoDBTable')
		print("table test exists")
		return "hakimbo"
	except dynamodb_client.exceptions.ResourceNotFoundException:
		print("table test not exists")
		return "makumbo"
	return "kojumbo"

