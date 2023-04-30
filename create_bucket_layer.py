import pulumi
import pulumi_aws as aws

def create_bucket_and_upload_layers():
    # Create an S3 bucket to store the layers
    bucket = aws.s3.Bucket('my-layers-bucket')

    # Upload pandas and scikit-learn layers to the S3 bucket
    pandas_layer = aws.s3.BucketObject('pd-layer',
                                       bucket=bucket.id,
                                       key='pandas-layer.zip',
                                       source=pulumi.FileAsset('layers/pandas-layer.zip'))

    sklearn_layer = aws.s3.BucketObject('sklearn-layer',
                                        bucket=bucket.id,
                                        key='sklearn-layer.zip',
                                        source=pulumi.FileAsset('layers/python.zip'))
    return bucket, pandas_layer, sklearn_layer
