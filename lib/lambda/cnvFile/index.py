import os
import uuid
import urllib
import boto3

import calculation


def get_bucketNameFromEnv(ENV_NAME):
    ret_ENV = ''

    try:
        ret_ENV = os.environ[ENV_NAME]
    except KeyError as e:
        return {
            "error": "Parameter name not exists"
        }
    return ret_ENV

def handler(event, context):
    s3c = boto3.client('s3')
    
    s3_up_bucket = get_bucketNameFromEnv('S3_PROCED_BUCKET_NAME')
    
    for record in event['Records']:
        hooking_bucket = record['s3']['bucket']['name']
        hooking_key = urllib.parse.unquote_plus(record['s3']['object']['key'])
        tmp_key = hooking_key.replace('/', '')
        
        up_key = 'out.png'
        rand = uuid.uuid4()
        dl_path = '/tmp/dl-{}{}'.format(rand, tmp_key) # download
        up_path = '/tmp/up-{}{}'.format(rand, tmp_key, up_key) # upload
        print(dl_path)
        print(up_path)
        s3c.download_file(hooking_bucket, hooking_key, dl_path)
        
        calculation.call_by_object(up_path, dl_path)
        
        s3c.upload_file(up_path, s3_up_bucket, up_key)
        
    return {
        "bucket: ": hooking_bucket,
        "key: ": hooking_key
    };
