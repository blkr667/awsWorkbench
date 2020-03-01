from troposphere import Template, Ref

from troposphere.iam import Role, InstanceProfile

from awacs.aws import Allow, Statement, Principal, PolicyDocument
from awacs.sts import AssumeRole



def create_template():
    template = Template()
    template.set_description('This stack deploys the OTM communication stack')
    template.set_version()
    template.set_transform('AWS::Serverless-2016-10-31')

    template.add_resource(Role(
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

    return template
