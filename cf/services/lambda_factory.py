from troposphere import Template, Ref, GetAtt
from troposphere.serverless import Function
from troposphere.iam import Role, Policy
from troposphere.awslambda import Environment
from troposphere.dynamodb import Table

def add_lambda(template: Template, role: Role, code_uri: str, lambda_name: str, dynamodb_table: Table) -> Function:
    return template.add_resource(Function(
        lambda_name,
        Handler=f'{lambda_name}.lambda_handler',
        Runtime="python3.6",
        CodeUri=code_uri,
        Timeout=10,
        Role=GetAtt(role, "Arn"),
        Environment = Environment(
            Variables={
                "TABLE_NAME": Ref(dynamodb_table)
            }
        )
    ))



