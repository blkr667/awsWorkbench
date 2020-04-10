from troposphere import Ref, Template, Output
from troposphere.apigateway import RestApi, Method
from troposphere.apigateway import Resource, MethodResponse
from troposphere.apigateway import Integration, IntegrationResponse
from troposphere.apigateway import Deployment, Stage, ApiStage
from troposphere.apigateway import UsagePlan, QuotaSettings, ThrottleSettings
from troposphere.apigateway import ApiKey, StageKey, UsagePlanKey
from troposphere.iam import Role, Policy
from troposphere.awslambda import Function, Code
from troposphere import GetAtt, Join


def add_method_to_apigateway(t: Template, lambda_function: Function, apigwlambda_role: Role, rest_api: RestApi, resource: Resource, method_type: str):
    return t.add_resource(Method(
        f'Method{lambda_function.name}',
        DependsOn=lambda_function,
        RestApiId=Ref(rest_api),
        AuthorizationType="NONE",
        ResourceId=Ref(resource),
        HttpMethod=method_type,
        Integration=Integration(
            Credentials=GetAtt(apigwlambda_role, "Arn"),
            Type="AWS",
            IntegrationHttpMethod='POST',
            IntegrationResponses=[
                IntegrationResponse(
                    StatusCode='200'
                )
            ],
            Uri=Join("", [
                "arn:aws:apigateway:eu-west-1:lambda:path/2015-03-31/functions/",
                GetAtt(lambda_function, "Arn"),
                "/invocations"
            ])
        ),
        MethodResponses=[
            MethodResponse(
                "CatResponse",
                StatusCode='200'
            )
        ]
    ))

def add_resource(t: Template, rest_api: RestApi):
    # Create a resource to map the lambda function to
    return t.add_resource(Resource(
        f'Resource{rest_api.name}',
        RestApiId=Ref(rest_api),
        PathPart="records",
        ParentId=GetAtt(rest_api.name, "RootResourceId"),
    ))

def add_apigateway_to_lambda(t: Template):
    # Create the Api Gateway
    rest_api = t.add_resource(RestApi(
        "RecordsApi",
        Name="ExampleApi"
    ))

    return rest_api


def add_deployment(t: Template, rest_api: RestApi, lambda_methods):
    # Create a deployment
    stage_name = 'v1'
    method_names = list(map(lambda lambda_method: lambda_method.name, lambda_methods))

    deployment = t.add_resource(Deployment(
        "%sDeployment" % stage_name,
        DependsOn=method_names,
        RestApiId=Ref(rest_api),
    ))

    stage = t.add_resource(Stage(
        '%sStage' % stage_name,
        StageName=stage_name,
        RestApiId=Ref(rest_api),
        DeploymentId=Ref(deployment)
    ))

    # Create an API usage plan
    usagePlan = t.add_resource(UsagePlan(
        "ExampleUsagePlan",
        UsagePlanName="ExampleUsagePlan",
        Description="Example usage plan",
        Quota=QuotaSettings(
            Limit=50000,
            Period="MONTH"
        ),
        Throttle=ThrottleSettings(
            BurstLimit=500,
            RateLimit=5000
        ),
        ApiStages=[
            ApiStage(
                ApiId=Ref(rest_api),
                Stage=Ref(stage)
            )]
    ))

    # Add the deployment endpoint as an output
    t.add_output([
        Output(
            "ApiEndpoint",
            Value=Join("", [
                "https://",
                Ref(rest_api),
                ".execute-api.eu-west-1.amazonaws.com/",
                stage_name
            ]),
            Description="Endpoint for this stage of the api"
        )
    ])
