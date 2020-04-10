from troposphere import Template, Ref

from cf.services import role_factory, lambda_factory, dynamodb_factory, apigateway_factory, s3_factory


def create_template():
    template = Template()
    template.set_description('This stack deploys the OTM communication stack')
    template.set_version()
    template.set_transform('AWS::Serverless-2016-10-31')

    # DB
    table = dynamodb_factory.add_dynamodb(template)

    # ROLES
    role_factory.add_role(template)
    use_dynamodb_role = role_factory.add_use_dynamodb_role(template)
    apigwlambda_role = role_factory.add_apigateway_role(template)

    # LAMBDAS
    add_record_lambda = lambda_factory.add_lambda(template, use_dynamodb_role, "./src/lambdas/records/add", "addRecordLambda", table)
    get_record_lambda = lambda_factory.add_lambda(template, use_dynamodb_role, "./src/lambdas/records/get", "getRecordLambda", table)
    remove_record_lambda = lambda_factory.add_lambda(template, use_dynamodb_role, "./src/lambdas/records/remove", "removeRecordLambda", table)



    # API GATEWAY METHODS
    rest_api = apigateway_factory.add_apigateway_to_lambda(template)
    resource = apigateway_factory.add_resource(template, rest_api)
    add_record_method = apigateway_factory.add_method_to_apigateway(template, add_record_lambda, apigwlambda_role, rest_api, resource, "GET")
    get_record_method = apigateway_factory.add_method_to_apigateway(template, get_record_lambda, apigwlambda_role, rest_api, resource, "POST")
    remove_record_method = apigateway_factory.add_method_to_apigateway(template, remove_record_lambda, apigwlambda_role, rest_api, resource, "DELETE")

    apigateway_factory.add_deployment(template, rest_api, [add_record_method, get_record_method, remove_record_method])

    bucket = s3_factory.add_bucket(template)

    return template
