#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import call

from cf import template_generator

TEMPLATE_FILE_NAME = "template.yaml"


def check_call(cmd):
    return_code = call(cmd)
    if return_code:
        exit(1)


def package():
    check_call(['aws',
                'cloudformation',
                'package',
                '--template-file',
                'template.json',
                '--s3-bucket',
                'bsources',
                '--s3-prefix',
                'lambdas/sample-blazej',
                '--output-template-file',
                'sam.yaml'])


def deploy():
    package()
    check_call(['aws',
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


print("start generating template")
if __name__ == "__main__":

    template_json = template_generator.generate_template_json()

    with open(TEMPLATE_FILE_NAME, 'w') as f:
        f.write(template_json)
    print('Cloudformation template saved at %s' % TEMPLATE_FILE_NAME)

    print('Execute2')
    deploy()