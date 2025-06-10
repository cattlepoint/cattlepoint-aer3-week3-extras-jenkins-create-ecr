#!/usr/bin/env python3
"""Delete a CloudFormation stack created from create-ecr-user.yaml.

Example:
    python delete-ecr-user-stack.py --stack-name ecr-user-stack --region us-east-1
"""

import argparse
import sys
import boto3
import botocore.exceptions


def delete_stack(stack_name: str, region: str) -> None:
    """Delete the specified CloudFormation stack and wait until it is gone."""
    cf = boto3.client("cloudformation", region_name=region)

    try:
        print(f"Deleting stack '{stack_name}' in region '{region}' …")
        cf.delete_stack(StackName=stack_name)

        waiter = cf.get_waiter("stack_delete_complete")
        waiter.wait(StackName=stack_name)
        print("Stack deletion complete.")
    except botocore.exceptions.ClientError as exc:
        print(f"Deletion failed: {exc.response['Error']['Message']}")
        sys.exit(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Delete an AWS CloudFormation stack")
    parser.add_argument(
        "--stack-name",
        default="ecr-user-stack",
        help="Name of the CloudFormation stack to delete (default: ecr-user-stack)",
    )
    parser.add_argument(
        "--region",
        default="us-east-1",
        help="AWS region where the stack resides (default: us-east-1)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    delete_stack(args.stack_name, args.region)


if __name__ == "__main__":
    main()
