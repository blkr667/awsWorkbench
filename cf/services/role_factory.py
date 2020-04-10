from troposphere import Template

from troposphere.iam import Role, Policy

from awacs.aws import Allow, Statement, Principal, PolicyDocument
from awacs.sts import AssumeRole
from awacs.dynamodb import DescribeTable, PutItem, GetRecords, GetItem, DeleteItem, Scan
from awacs.logs import CreateLogGroup, CreateLogStream, PutLogEvents


def add_role(template: Template) -> Role:
    return template.add_resource(Role(
        "CFNRole",
        AssumeRolePolicyDocument=PolicyDocument(
            Statement=[
                Statement(
                    Effect=Allow,
                    Action=[AssumeRole],
                    Principal=Principal("Service", ["ec2.amazonaws.com"])
                )
            ]
        )
    ))


def add_use_dynamodb_role(template: Template) -> Role:
    return template.add_resource(Role(
        "usedynamodbrole",
        AssumeRolePolicyDocument=PolicyDocument(
            Statement=[
                Statement(
                    Effect=Allow,
                    Action=[AssumeRole],
                    Principal=Principal("Service", ["lambda.amazonaws.com"])
                ),
                Statement(
                    Effect=Allow,
                    Action=[AssumeRole],
                    Principal=Principal("Service", ["apigateway.amazonaws.com"])
                )
            ]
        ),
        Policies=[
            Policy(
                PolicyName="policy_use_dynamodb",
                PolicyDocument=PolicyDocument(
                    Id="policy_use_dynamodb",
                    Version="2012-10-17",
                    Statement=[
                        Statement(
                            Effect=Allow,
                            Action=[DescribeTable, PutItem, GetRecords, GetItem, DeleteItem, Scan],
                            Resource=["*"]
                        ),
                        Statement(
                            Effect=Allow,
                            Action=[CreateLogGroup, CreateLogStream, PutLogEvents],
                            Resource=["*"]
                        )
                    ]
                )
            )
        ]
    ))

def add_apigateway_role(template: Template) -> Role:
    # Create a role for the lambda function
    return template.add_resource(Role(
        "LambdaExecutionRole",
        Path="/",
        Policies=[Policy(
            PolicyName="root",
            PolicyDocument={
                "Version": "2012-10-17",
                "Statement": [{
                    "Action": ["logs:*"],
                    "Resource": "arn:aws:logs:*:*:*",
                    "Effect": "Allow"
                }, {
                    "Action": ["lambda:*"],
                    "Resource": "*",
                    "Effect": "Allow"
                }]
            })],
        AssumeRolePolicyDocument={"Version": "2012-10-17", "Statement": [
            {
                "Action": ["sts:AssumeRole"],
                "Effect": "Allow",
                "Principal": {
                    "Service": [
                        "lambda.amazonaws.com",
                        "apigateway.amazonaws.com"
                    ]
                }
            }
        ]},
    ))
