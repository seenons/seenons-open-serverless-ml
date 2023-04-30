import boto3
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import io
import datetime

s3 = boto3.client('s3')


def lambda_handler(event, context):
    print("Pandas", pd.__version__)
    print("Numpy", np.__version__)

    # Get the S3 bucket and key from the PUT event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    print(f'Bucket: {bucket}')
    print(f'Key: {key}')

    # Read the file from S3 and load it into a Pandas DataFrame
    file = s3.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(io.BytesIO(file['Body'].read()))
    df['ratio'] = df['tonsRecycled'] / df['tons']

    clf = IsolationForest(random_state=42, contamination='auto')
    #cols = ['tonsRecycled', 'tons', 'ratio']
    cols = ['tons', 'tonsRecycled']
    clf.fit(df[cols])

    df['anomaly'] = list(map(lambda x: True if x == -1 else False, clf.predict(df[cols])))
    print("Anomaly ratio:", df['anomaly'].value_counts(normalize=True))

    # Store the processed data back to S3
    job = f"job_{datetime.datetime.now()}"
    processed_data = df.to_csv(index=False)
    processed_key = f'output/{job}/{key.split("/")[-1]}'
    s3.put_object(Bucket=bucket, Key=processed_key, Body=processed_data.encode())
    print(f"Stored results in S3: {bucket}/{processed_key}")
    return {
        'statusCode': 200,
        'lines': df.shape[0]
    }
