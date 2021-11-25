import os
import json
import uuid
import urllib
import boto3


import numpy as np
from PIL import Image

def imgPath2mat_rRGB(path):
    imgRaw = Image.open(path)
    imgRGB = imgRaw.split()
    imgR = imgRGB[0]
    imgG = imgRGB[1]
    imgB = imgRGB[2]
    return (imgR, imgG, imgB)

def mat_rRGB2img(path, imgR, imgG, imgB):
    imgCombined = np.dstack((np.dstack((imgR, imgG)), imgB))
    imgPIL      = Image.fromarray(imgCombined)
    imgPIL.save(path)


def get_bucketNameFromEnv(ENV_NAME):
    ret_ENV = ''

    try:
        ret_ENV = os.environ[ENV_NAME]
    except KeyError as e:
        return {
            "error": "Parameter name not exists"
        }
    return ret_ENV

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


def call_by_object(up_path, dl_path):

    # cnv img
    imgR, imgG, imgB = imgPath2mat_rRGB(dl_path)
    imgG = 0.5 * imgG
    mat_rRGB2img(up_path, imgR, imgG, imgB)
    
    return

def handler(event, context):
    s3c = boto3.client('s3')
    
    s3_up_bucket = get_bucketNameFromEnv('S3_PROCED_BUCKET_NAME')
    
    for record in event['Records']:
        hooking_bucket = record['s3']['bucket']['name']
        hooking_key = urllib.parse.unquote_plus(record['s3']['object']['key'])
        tmp_key = hooking_key.replace('/', '')
        
        rand = uuid.uuid4()
        dl_path = '/tmp/dl-{}{}'.format(rand, tmp_key) # download
        up_path = '/tmp/up-{}'.format(rand, tmp_key) # upload
        print(dl_path)
        print(up_path)
        s3c.download_file(hooking_bucket, hooking_key, dl_path)
        
        call_by_object(up_path, dl_path)

        up_key = '2021_1126.txt'
        s3c.upload_file(up_path, '{}'.format(s3_up_bucket), up_key)
        
    return {
        "bucket: ": hooking_bucket,
        "key: ": hooking_key
    };
