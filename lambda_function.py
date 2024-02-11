import boto3

def lambda_handler(event, context):
    # Create EMR client
    emr = boto3.client('emr')

    # Define EMR cluster configuration
    cluster_config = {
        'Name': 'Test-EMR',
        'ReleaseLabel': 'emr-6.2.0',  # Example release label
        'Applications': [
            {
                'Name': 'Spark'
            },
            # Add other applications as needed
        ],
        'Instances': {
            'InstanceGroups': [
                {
                    'Name': 'Master',
                    'InstanceRole': 'MASTER',
                    'InstanceType': 'm5.xlarge',
                    'InstanceCount': 1
                },
                {
                    'Name': 'Core',
                    'InstanceRole': 'CORE',
                    'InstanceType': 'm5.xlarge',
                    'InstanceCount': 2
                }
                # Add other instance groups as needed
            ],
            'Ec2KeyName': 'aws_login',
            'KeepJobFlowAliveWhenNoSteps': True,
            'TerminationProtected': False
        },
        'JobFlowRole': 'EMR-Role',
        'ServiceRole': 'EMR-Role'
        # Add additional configuration parameters as needed
    }

    # Create EMR cluster
    response = emr.run_job_flow(**cluster_config)

    # Extract cluster ID from the response
    cluster_id = response['JobFlowId']

    return {
        'statusCode': 200,
        'body': f'EMR Cluster {cluster_id} created successfully.'
    }
