import * as cdk from '@aws-cdk/core';
import * as s3 from '@aws-cdk/aws-s3';
import * as s3notify from '@aws-cdk/aws-s3-notifications'
import * as lambda from '@aws-cdk/aws-lambda';


export class InfraStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // S3 bucket
    const s3_raw_bucket = new s3.Bucket(this, 's3-raw-bucket', {
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    })
    
    const s3_proced_bucket = new s3.Bucket(this, 's3-proced-bucket', {
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    })

    // lambda function triggered by s3 hook
    const s3_hook_lambda = new lambda.Function(this, 's3-hook-lambda', {
      runtime: lambda.Runtime.PYTHON_3_8,
      code: lambda.Code.fromAsset('lib/lambda/cnvFile/deployment-package.zip'),
      handler: 'index.handler',
      environment: {
	S3_PROCED_BUCKET_NAME: s3_proced_bucket.bucketName
      }
    });
    s3_raw_bucket.addObjectCreatedNotification(new s3notify.LambdaDestination(s3_hook_lambda))
    s3_raw_bucket.grantRead(s3_hook_lambda) // CreatedNotification により lambda が再帰呼び出しできないように，read か write のみ付与する
    s3_proced_bucket.grantWrite(s3_hook_lambda) // CreatedNotification により lambda が再帰呼び出しできないように，read か write のみ付与する
  }
}

