pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = 'us-east-1' // replace 'your-region' with your AWS region
        AWS_ROLE_ARN = 'arn:aws:iam::743292407330:role/Local-Jenkins-Role' // replace with your role ARN
        LAMBDA_ROLE_ARN = 'arn:aws:iam::743292407330:role/service-role/myLambdaRole'
        AWS_ROLE_SESSION_NAME = 'jenkins-session'
        LAMBDA_FUNCTION_NAME = 'lambda_function'
        HANDLER_FUNCTION = 'lambda_function.lambda_handler'
        LAMBDA_RUNTIME = 'python3.8' // e.g., 'nodejs14.x', 'python3.8', etc.
        ZIP_FILE_NAME = 'lambda_function' // Name of the zip file
        SOURCE_FOLDER = './' // Path to your Lambda function code
 	    S3_BUCKET_NAME = 'test-lambdarole'
	    S3_EVENT_TYPE = 's3:ObjectCreated:*'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/greatbuzzaman/aws-test.git']]])
            }
        }

        stage('Assume Role') {
            steps {
                script {
                    def stsResponse = sh(script: "/usr/local/bin/aws sts assume-role --role-arn ${AWS_ROLE_ARN} --role-session-name JenkinsLambdaSession", returnStdout: true).trim()
                    def credentials = new groovy.json.JsonSlurper().parseText(stsResponse)

                    // Set temporary credentials as environment variables
                    env.AWS_ACCESS_KEY_ID = credentials.Credentials.AccessKeyId
                    env.AWS_SECRET_ACCESS_KEY = credentials.Credentials.SecretAccessKey
                    env.AWS_SESSION_TOKEN = credentials.Credentials.SessionToken
                }
            }
        }
        
        stage('Create Lambda Package') {
            steps {
                script {
                    // Navigate to the source folder and create a zip file
                    sh "cd ${SOURCE_FOLDER} && zip -r ${ZIP_FILE_NAME} ./*"
                    sh " pwd "
                    sh " ls -lhrt /Users/amansharma/.jenkins/workspace/AWS-Create-Services/"
                }
            }
        }
        
        stage('Deploy Lambda') {
            steps {
                script {
                    // Define your Lambda function details
                    //def lambdaName = 'test-lambda'
                    //def handler = 'lambda.py'
                    //def runtime = 'python3.8' // e.g., 'nodejs14.x', 'python3.8', etc.
                    //def zipFile = 'lambda_function.zip' // Path to your Lambda function code

                    // Command to create or update the Lambda function
                    def awsCliCommand = "/usr/local/bin/aws lambda create-function --function-name ${LAMBDA_FUNCTION_NAME} --runtime ${LAMBDA_RUNTIME} --handler ${HANDLER_FUNCTION} --zip-file fileb://${WORKSPACE}/${ZIP_FILE_NAME}.zip --role ${LAMBDA_ROLE_ARN} --region ${AWS_DEFAULT_REGION}"

                    // Execute the AWS CLI command
                    sh awsCliCommand
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                script {
                    // Command to describe the Lambda function to verify its deployment
                    def describeLambdaCommand = "/usr/local/bin/aws lambda get-function --function-name ${LAMBDA_FUNCTION_NAME} --region ${AWS_DEFAULT_REGION}"

                    // Execute the AWS CLI command
                    sh describeLambdaCommand
                }
            }
        }
        stage('Add S3 Trigger') {
            steps {
                script {
                    // Use AWS CLI to add S3 trigger to Lambda function
                    
                    sh "/usr/local/bin/aws lambda add-permission --function-name ${LAMBDA_FUNCTION_NAME} --statement-id s3-trigger --action lambda:InvokeFunction --principal s3.amazonaws.com --source-arn arn:aws:s3:::${S3_BUCKET_NAME} --region ${AWS_DEFAULT_REGION}"

                    //sh "/usr/local/bin/aws s3api put-bucket-notification-configuration --bucket ${S3_BUCKET_NAME} --notification-configuration \"{\"LambdaFunctionConfigurations\":[{\"LambdaFunctionArn\":\"arn:aws:lambda:${AWS_DEFAULT_REGION}:743292407330:function:${LAMBDA_FUNCTION_NAME}\",\"Events\":[\"${S3_EVENT_TYPE}\"]}]}\""

                    sh "aws s3api put-bucket-notification-configuration --bucket ${S3_BUCKET_NAME} --notification-configuration '{\"LambdaFunctionConfigurations\":[{\"LambdaFunctionArn\":\"arn:aws:lambda:${AWS_DEFAULT_REGION}:743292407330:function:${LAMBDA_FUNCTION_NAME}\",\"Events\":[\"s3:ObjectCreated:*\"]}]}\""

                }
            }
        }
    }
}
