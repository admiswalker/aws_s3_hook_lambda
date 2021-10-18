import * as cdk from '@aws-cdk/core';
import * as s3 from '@aws-cdk/aws-s3';
import * as lambda from '@aws-cdk/aws-lambda';
import * as lambdaES from '@aws-cdk/aws-lambda-event-sources';

/*
function gen_s3bucket(scope: cdk.Construct): [s3.Bucket, s3.Bucket] {
  const s3_rawBucket = new s3.Bucket(scope, 'raw_bucket', {
    removalPolicy: cdk.RemovalPolicy.DESTROY
  });

  const s3_procedBucket = new s3.Bucket(scope, 'preprocessed_bucket', {
    removalPolicy: cdk.RemovalPolicy.DESTROY
  });

  return [s3_rawBucket, s3_procedBucket];
}

function gen_lambda_s3Hook(scope: cdk.Construct, s3_rawBucket: s3.Bucket, s3_procedBucket: s3.Bucket): void {
  const fn = new lambda.Function(scope, 'lambda_s3Hook', {
    runtime: lambda.Runtime.NODEJS_14_X, 
    code: lambda.Code.fromAsset('lib/lambda/cnvFile'),
    handler: 'index.handler'
  });
  
  fn.addEventSource(new lambdaES.S3EventSource(s3_rawBucket, {
    events: [s3.EventType.OBJECT_CREATED]
  }));
}

export class InfraStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // S3 bucket
    var s3_rawBucket: s3.Bucket;
    var s3_procedBucket: s3.Bucket;
    [s3_rawBucket, s3_procedBucket] = gen_s3bucket(this);
    
    // lambda triggered by s3 hook
    gen_lambda_s3Hook(this, s3_rawBucket, s3_procedBucket);
  }
}
*/


export class InfraStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // S3 bucket
    const s3_rawBucket = new s3.Bucket(this, 's3_rawBucket', {
      removalPolicy: cdk.RemovalPolicy.DESTROY
    })
    
    const s3_procedBucket = new s3.Bucket(this, 's3_preprocessedBucket', {
      removalPolicy: cdk.RemovalPolicy.DESTROY
    });
    
    // lambda triggered by s3 hook
    const s3Hook_lambda = new lambda.Function(this, 's3Hook_lambda', {
      runtime: lambda.Runtime.PYTHON_3_8,
      code: lambda.Code.fromAsset('lib/lambda/cnvFile'),
      handler: 'index.handler'
    });
    
    s3Hook_lambda.addEventSource(new lambdaES.S3EventSource(s3_rawBucket, {
      events: [s3.EventType.OBJECT_CREATED]
    }));
    
  }
}

