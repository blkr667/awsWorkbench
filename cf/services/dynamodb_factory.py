from troposphere import Output, Parameter, Ref, Template
from troposphere.dynamodb import (KeySchema, AttributeDefinition,
                                  ProvisionedThroughput)
from troposphere.dynamodb import Table


def add_dynamodb(template: Template) -> Table:
    hash_key_name = template.add_parameter(Parameter(
        "HashKeyElementName",
        Description="HashType PrimaryKey Name",
        Type="String",
        AllowedPattern="[a-zA-Z0-9]*",
        MinLength="1",
        MaxLength="2048",
        Default="date",
        ConstraintDescription="must contain only alphanumberic characters"
    ))

    hash_key_type = template.add_parameter(Parameter(
        "HashKeyElementType",
        Description="HashType PrimaryKey Type",
        Type="String",
        Default="S",
        AllowedPattern="[S|N]",
        MinLength="1",
        MaxLength="10",
        ConstraintDescription="must be either S or N"
    ))

    read_units = template.add_parameter(Parameter(
        "ReadCapacityUnits",
        Description="Provisioned read throughput",
        Type="Number",
        Default="5",
        MinValue="5",
        MaxValue="10000",
        ConstraintDescription="should be between 5 and 10000"
    ))

    write_units = template.add_parameter(Parameter(
        "WriteCapacityUnits",
        Description="Provisioned write throughput",
        Type="Number",
        Default="10",
        MinValue="5",
        MaxValue="10000",
        ConstraintDescription="should be between 5 and 10000"
    ))

    my_dynamodb = template.add_resource(Table(
        "myDynamoDBTable",
        AttributeDefinitions=[
            AttributeDefinition(
                AttributeName=Ref(hash_key_name),
                AttributeType=Ref(hash_key_type)
            ),
        ],
        KeySchema=[
            KeySchema(
                AttributeName=Ref(hash_key_name),
                KeyType="HASH"
            )
        ],
        ProvisionedThroughput=ProvisionedThroughput(
            ReadCapacityUnits=Ref(read_units),
            WriteCapacityUnits=Ref(write_units)
        )
    ))

    template.add_output(Output(
        "TableName",
        Value=Ref(my_dynamodb),
        Description="Table name of the newly create DynamoDB table",
    ))

    return my_dynamodb
