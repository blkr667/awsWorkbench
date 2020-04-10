#!/usr/bin/env python
# -*- coding: utf-8 -*-
import boto3
import os

from botocore.exceptions import ClientError

client = boto3.client('cloudformation')
current_path = os.getcwd()

def copy_bundle_to_s3(bundle_subdirectory, aws_region, bucket_name):

    target_dir = current_path + bundle_subdirectory

    if not os.path.isdir(target_dir):
        raise ValueError('target_dir %r not found.' % target_dir)

    s3 = boto3.resource('s3', region_name=aws_region)

    print("coping files")
    for filename in os.listdir(target_dir):

        print(filename)
        print('Uploading %s to Amazon S3 bucket %s' % (filename, bucket_name))
        s3.Object(bucket_name, filename).put(Body=open(os.path.join(target_dir, filename), 'rb'))

        print('File uploaded to https://s3.%s.amazonaws.com/%s/%s' % (
            aws_region, bucket_name, filename))