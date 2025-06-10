#!/usr/bin/env python3
import boto3
import botocore

stack_name = 'ECRListCreateUser'
template_file = 'create-ecr-user.yaml'

cf = boto3.client('cloudformation')

with open(template_file) as f:
    template_body = f.read()

def deploy():
    try:
        cf.create_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Capabilities=['CAPABILITY_NAMED_IAM']
        )
        waiter = cf.get_waiter('stack_create_complete')
    except botocore.exceptions.ClientError as e:
        if 'AlreadyExistsException' in str(e):
            cf.update_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Capabilities=['CAPABILITY_NAMED_IAM']
            )
            waiter = cf.get_waiter('stack_update_complete')
        elif 'No updates are to be performed' in str(e):
            return
        else:
            raise
    waiter.wait(StackName=stack_name)

def fetch_keys():
    outputs = cf.describe_stacks(StackName=stack_name)['Stacks'][0]['Outputs']
    kv = {o['OutputKey']: o['OutputValue'] for o in outputs}
    print('AccessKeyId:', kv['AccessKeyId'])
    print('SecretAccessKey:', kv['SecretAccessKey'])

if __name__ == '__main__':
    deploy()
    fetch_keys()
