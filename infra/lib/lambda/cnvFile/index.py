import json
import urllib.parse
import boto3

def get_hookingBucketNameAndKey(event):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    return bucket, key

def readObject(bucket, key='out.txt'):
    s3 = boto3.client('s3')
    print('bucket: %s' % bucket)
    print('key: %s' % key)
    
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
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
'''
def writeObject(bucket, key='out.txt'):
    obj = bucket.Object(fname)
    obj = s3.Object(bucket, key='out.txt')
    obj.put( Body='Hello AWS S3!' )
    return
'''
def handler(event, context):
    hooking_bucket, hooking_key = get_hookingBucketNameAndKey(event)
    size, body = readObject(hooking_bucket, hooking_key)
    print('--- printing object: begin ---')
    print('response:', size, body)
    print('--- printing object: end ---')
    
#    writeObject(bucket, key='out.txt')
    
    return {
        "bucket: ": hooking_bucket,
        "key: ": hooking_key
    };

