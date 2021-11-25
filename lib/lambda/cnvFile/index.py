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
    print('')
    print('--- dl_path ---')
    print(dl_path)
    print('')
    
    print('--- up_path ---')
    print(up_path)
    print('')
    cmd = ('touch %s' % up_path)
    os.system(cmd)
    cmd = ('echo "abcdef2021_1126" >> %s' % up_path)
    os.system(cmd)
    return

#def mkdir(path):
#    os.makedirs(path, exist_ok=True)

def handler(event, context):
    s3c = boto3.client('s3')
#    s3r = boto3.resource('s3')
    
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
        
    '''
    size, body = readObject(hooking_bucket, hooking_key)
    print('--- printing object: begin ---')
    print('response:', size, body)
    print('--- printing object: end ---')

    path_r=io.BytesIO(body)
    imgR, imgG, imgB = imgPath2mat_rRGB(path_r)
    imgG = 0.5 * imgG
    raw_w
    path_w=io.BytesIO(raw_w)
    mat_rRGB2img(path_w, imgR, imgG, imgB)
    '''
    
    return {
        "bucket: ": hooking_bucket,
        "key: ": hooking_key
    };
