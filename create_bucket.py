import pulumi
import pulumi_aws as aws

BUCKET = "poc-anomalies-serverless-rrc-bucket"


def create_bucket_for_lambda(lambda_function):
    # Create the S3 bucket
    bucket = aws.s3.BucketV2(BUCKET)

    # Create the 'input' and 'output' folders
    input_folder = aws.s3.BucketObject('input-folder',
                                       bucket=bucket.id,
                                       key='input/')

    output_folder = aws.s3.BucketObject('output-folder',
                                        bucket=bucket.id,
                                        key='output/')
    input_file = aws.s3.BucketObject('input.csv',
                                     bucket=bucket.id,
                                     key='input/input.csv',
                                     source=pulumi.FileAsset('data/input.csv'))

    allow_bucket = aws.lambda_.Permission("allowBucket",
                                          action="lambda:InvokeFunction",
                                          function=lambda_function.arn,
                                          principal="s3.amazonaws.com",
                                          source_arn=bucket.arn)
    # Configure the S3 bucket to trigger the Lambda function on object upload
    bucket_notification = aws.s3.BucketNotification(f"{BUCKET}-notification",
                                                    bucket=bucket.id,
                                                    lambda_functions=[aws.s3.BucketNotificationLambdaFunctionArgs(
                                                        lambda_function_arn=lambda_function.arn,
                                                        events=['s3:ObjectCreated:*'],
                                                        filter_prefix='input/')],
                                                    opts=pulumi.ResourceOptions(depends_on=[allow_bucket]))

    # Export the bucket name and the keys of the input and output folders
    pulumi.export('bucket_name', bucket.id)
    pulumi.export('input_folder_key', input_folder.id)
    pulumi.export('output_folder_key', output_folder.id)
