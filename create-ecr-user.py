#!/usr/bin/env python3
import boto3
import botocore

STACK_NAME = "ECRListCreateUser"
TEMPLATE_FILE = "create-ecr-user.yaml"

cf = boto3.client("cloudformation")

with open(TEMPLATE_FILE) as f:
    TEMPLATE_BODY = f.read()

def deploy():
    try:
        cf.create_stack(
            StackName=STACK_NAME,
            TemplateBody=TEMPLATE_BODY,
            Capabilities=["CAPABILITY_NAMED_IAM"],
        )
        waiter = cf.get_waiter("stack_create_complete")
    except botocore.exceptions.ClientError as e:
        if 'AlreadyExistsException' in str(e):
            cf.update_stack(
                StackName=STACK_NAME,
                TemplateBody=TEMPLATE_BODY,
                Capabilities=["CAPABILITY_NAMED_IAM"],
            )
            waiter = cf.get_waiter("stack_update_complete")
        elif "No updates are to be performed" in str(e):
            return
        else:
            raise
    waiter.wait(StackName=STACK_NAME)

def fetch_keys():
    outputs = cf.describe_stacks(StackName=STACK_NAME)["Stacks"][0]["Outputs"]
    kv = {o['OutputKey']: o['OutputValue'] for o in outputs}
    print('AccessKeyId:', kv['AccessKeyId'])
    print('SecretAccessKey:', kv['SecretAccessKey'])

def main() -> None:
    deploy()
    fetch_keys()


if __name__ == "__main__":
    main()
