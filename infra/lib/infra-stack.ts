import * as cdk from '@aws-cdk/core';
import * as s3 from '@aws-cdk/aws-s3';

function gen_s3bucket(scope: cdk.Construct): void {
  const s3_raw_bucket = new s3.Bucket(scope, 'raw_bucket', {
    removalPolicy: cdk.RemovalPolicy.DESTROY
  });

  const s3_preprocessed_bucket = new s3.Bucket(scope, 'preprocessed_bucket', {
    removalPolicy: cdk.RemovalPolicy.DESTROY
  });
}

function gen_lambda(scope: cdk.Construct): void {
  const hello = new lambda.Function(this, 'HelloHandler', {
    runtime: lambda.Runtime.NODEJS_14_X, 
    code: lambda.Code.fromAsset('lib/lambda/hello'),
    handler: 'index.handler'
  });
}

export class InfraStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // S3 bucket
    gen_s3bucket(this);
    
    // lambda triggered by s3 hook
    gen_lambda(this);
  }
}
