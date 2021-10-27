import json
import urllib.parse
import boto3

print('Loading function')

s3 = boto3.client('s3')


def handler(event, context):
    print('in index handler')
    print(event)
    print(context)
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    print('bucket: %s' % bucket)
    print('key: %s' % key)
    
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

    print('--- printing object: begin ---')
    print(response['ContentType'])
    print(response.decode('utf-8'))
    print('--- printing object: end ---')
    
    return {
        "bucket: ": bucket,
        "key: ": key
    };

