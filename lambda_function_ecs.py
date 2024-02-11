import boto3

ecs = boto3.client('ecs')

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        # Trigger ECS task
        response = ecs.run_task(
            cluster='spark-test-ecs',
            taskDefinition='your-task-definition-arn',
            overrides={
                'containerOverrides': [
                    {
                        'name': 'test-container',
                        'command': ['spark-submit', '--master', 'local[*]', '/app/spark_code.py'],
                        'environment': [
                            {
                                'name': 'AWS_ACCESS_KEY_ID',
                                'value': 'your-aws-access-key-id'
                            },
                            {
                                'name': 'AWS_SECRET_ACCESS_KEY',
                                'value': 'your-aws-secret-access-key'
                            },
                            {
                                'name': 'SPARK_INPUT_PATH',
                                'value': f's3a://{bucket}/{key}'
                            },
                            {
                                'name': 'SPARK_OUTPUT_PATH',
                                'value': 's3a://test-lambdarole/ecs-output/'
                            }
                        ]
                    }
                ]
            }
        )
        print(response)
