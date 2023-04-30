"""An AWS Python Pulumi program"""
from create_bucket_layer import create_bucket_and_upload_layers
from create_lambda import create_lambda
from create_bucket import create_bucket_for_lambda

bucket, pandas_layer, sklearn_layer = create_bucket_and_upload_layers()
lambda_function = create_lambda(bucket, pandas_layer, sklearn_layer)
create_bucket_for_lambda(lambda_function)

