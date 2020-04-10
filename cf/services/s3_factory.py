from troposphere import GetAtt, Join, Output, Template
from troposphere.s3 import Bucket, PublicRead, WebsiteConfiguration
from troposphere import Output, Parameter, Ref, Template


def add_bucket(template: Template) -> Bucket:
    bucket = template.add_resource(Bucket(
        "recordsui",
        AccessControl=PublicRead,
        WebsiteConfiguration=WebsiteConfiguration(
            IndexDocument="index.html",
            ErrorDocument="error.html"
        )
    ))

    template.add_output([
        Output(
            "WebsiteURL",
            Value=GetAtt(bucket, "WebsiteURL"),
            Description="URL for website hosted on S3"
        ),
        Output(
            "S3BucketSecureURL",
            Value=Join("", ["http://", GetAtt(bucket, "DomainName")]),
            Description="Name of S3 bucket to hold website content"
        ),
    ])

    return bucket
