pipeline {
    agent any

    parameters {
        string(name: 'ECR_REPO_NAME', defaultValue: 'my-app', description: 'ECR repository name')
    }

    environment {
        AWS_DEFAULT_REGION = 'us-east-1'              // adjust if needed
        STACK_NAME        = 'CreateECRRepo'
        TEMPLATE_FILE     = 'ecr-repo.yaml'           // CloudFormation template in repo
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Deploy ECR via CloudFormation') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'ecr-create'
                ]]) {
                    sh """
                        aws cloudformation deploy \
                          --template-file ${TEMPLATE_FILE} \
                          --stack-name ${STACK_NAME} \
                          --parameter-overrides RepositoryName=${params.ECR_REPO_NAME} \
                          --capabilities CAPABILITY_NAMED_IAM
                    """
                }
            }
        }

        stage('Show Outputs') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'ecr-create'
                ]]) {
                    sh """
                        aws cloudformation describe-stacks \
                          --stack-name ${STACK_NAME} \
                          --query 'Stacks[0].Outputs' \
                          --output table
                    """
                }
            }
        }
    }
}
