#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import call
import boto3

from cf import template_generator
from ui_bundle_copy import copy_bundle_to_s3
import os

TEMPLATE_FILE_NAME = "template.yaml"
AWS_REGION = "eu-west-1"
UI_BUNDLE_SUBDIRECTORY = "./ui/stats-app/dist/stats-app"

client = boto3.client('cloudformation')


def check_call(cmd):
    return_code = call(cmd)
    if return_code:
        exit(1)


def package():
    call(['aws',
          'cloudformation',
          'package',
          '--template-file',
          'template.yaml',
          '--s3-bucket',
          'bsources',
          '--s3-prefix',
          'lambdas/sample-blazej',
          '--output-template-file',
          'sam.yaml'])


def deploy():
    package()
    call(['aws',
          'cloudformation',
          'deploy',
          '--template-file',
          'sam.yaml',
          '--stack-name',
          'blazej-stack2',
          '--capabilities',
          'CAPABILITY_IAM',
          '--capabilities',
          'CAPABILITY_NAMED_IAM'])


is_windows = os.name == 'nt'

print("start generating template")
if __name__ == "__main__":
    template = template_generator.generate()

    template_json = template.to_json()

    with open(TEMPLATE_FILE_NAME, 'w') as f:
        f.write(template_json)
    print('Cloudformation template saved at %s' % TEMPLATE_FILE_NAME)
    print('Execute2')
    deploy()
    print('ui bundle coping start')

    call(['aws', 's3', 'sync', UI_BUNDLE_SUBDIRECTORY,
          's3://blazej-stack2-recordsui-1aepc8pupm3iy/',
          '--acl',
          'public-read'],
         shell=is_windows)
