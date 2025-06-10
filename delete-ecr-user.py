#!/usr/bin/env python3
"""Delete the CloudFormation stack created from ``create-ecr-user.yaml``."""

import boto3
import botocore.exceptions


STACK_NAME = "ECRListCreateUser"

cf = boto3.client("cloudformation")


def delete_stack(stack_name: str) -> None:
    """Delete the specified CloudFormation stack and wait until it is gone."""

    try:
        print(f"Deleting stack '{stack_name}' …")
        cf.delete_stack(StackName=stack_name)

        waiter = cf.get_waiter("stack_delete_complete")
        waiter.wait(StackName=stack_name)
        print("Stack deletion complete.")
    except botocore.exceptions.ClientError as exc:
        print(f"Deletion failed: {exc.response['Error']['Message']}")
        raise


def main() -> None:
    delete_stack(STACK_NAME)


if __name__ == "__main__":
    main()
