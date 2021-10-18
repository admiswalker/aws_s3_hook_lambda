import boto3

print('Loading function')

s3 = boto3.client('s3')


def handler(event, context):
    print('in index handler')
    
    bucket = event.bucket
    key = event.key    
    return {
        "bucket: ": bucket,
        "key: ": key
    };

