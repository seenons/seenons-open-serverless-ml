import pulumi
import pulumi_aws as aws

ARCHITECTURE = 'x86_64'
VERSION = "python3.9"


def create_lambda(layers_bucket, pd_layer, sklearn_layer):
    lambda_role, lambda_policy_arns = create_role()

    for policy_arn in lambda_policy_arns:
        policy_attachment = aws.iam.RolePolicyAttachment(f'lambda-policy-{policy_arn}',
                                                         policy_arn=policy_arn,
                                                         role=lambda_role.name)

    function_layers = [
        aws.lambda_.LayerVersion('pandas-layer',
                                 layer_name='pandas',
                                 compatible_runtimes=[VERSION],
                                 compatible_architectures=[ARCHITECTURE],
                                 s3_bucket=layers_bucket.id,
                                 s3_key=pd_layer.key,
                                 ),
        aws.lambda_.LayerVersion('sklearn-layer',
                                 layer_name='sklearn',
                                 compatible_runtimes=[VERSION],
                                 compatible_architectures=[ARCHITECTURE],
                                 s3_bucket=layers_bucket.id,
                                 s3_key=sklearn_layer.key,
                                 ),
    ]

    # Create a new Lambda function
    function = aws.lambda_.Function(
        resource_name='anomalies-function',
        runtime=VERSION,
        code=pulumi.AssetArchive({'.': pulumi.FileArchive('./lambda')}),
        handler="lambda_function.lambda_handler",
        architectures=[ARCHITECTURE],
        timeout=300,
        memory_size=1024,
        role=lambda_role.arn,
        layers=function_layers
    )

    pulumi.export('function_arn', function.arn)
    return function


def create_role():
    lambda_role = aws.iam.Role('lambda-role',
                               assume_role_policy="""{
                                   "Version": "2012-10-17",
                                   "Statement": [
                                       {
                                           "Effect": "Allow",
                                           "Principal": {
                                               "Service": "lambda.amazonaws.com"
                                           },
                                           "Action": "sts:AssumeRole"
                                       }
                                   ]
                               }""")

    # Attach the necessary policies to the IAM role
    lambda_policy_arns = [
        'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole',
        'arn:aws:iam::aws:policy/AmazonS3FullAccess',  # Add any other necessary policies
    ]
    return lambda_role, lambda_policy_arns
