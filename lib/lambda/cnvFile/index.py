import os
import json
import urllib.parse
import boto3

def get_bucketNameFromEnv():
    S3_PROCED_BUCKET_NAME = ''

    try:
        S3_PROCED_BUCKET_NAME = os.environ['S3_PROCED_BUCKET_NAME']
    except KeyError as e:
        return {
            "error": "Parameter name not exists"
        }
    return S3_PROCED_BUCKET_NAME

def get_hookingBucketNameAndKey(event):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    return bucket, key

def readObject(bucket, key='out.txt'):
    s3c = boto3.client('s3')
    print('bucket: %s' % bucket)
    print('key: %s' % key)
    
    try:
        response = s3c.get_object(Bucket=bucket, Key=key)
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

    # httpStatusCode = response['ResponseMetadata']['HTTPStatusCode']
    # lastModified = response['LastModified']
    # contentType = response['ContentType']
    size = response['ContentLength']
    body = response['Body'].read()
    return size, body

def writeObject(bucket, key='out.txt'):
    s3r = boto3.resource('s3')
    obj = s3r.Object(bucket, key='out.txt')
    obj.put( Body='Hello AWS S3!' )
    return

def handler(event, context):
    hooking_bucket, hooking_key = get_hookingBucketNameAndKey(event)
    size, body = readObject(hooking_bucket, hooking_key)
    print('--- printing object: begin ---')
    print('response:', size, body)
    print('--- printing object: end ---')

    s3_proced_bucket = get_bucketNameFromEnv()
    writeObject(s3_proced_bucket, key='out.txt')
    
    return {
        "bucket: ": hooking_bucket,
        "key: ": hooking_key
    };

