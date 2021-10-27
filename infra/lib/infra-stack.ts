import * as cdk from '@aws-cdk/core';
import * as iam from "@aws-cdk/aws-iam";
import * as s3 from '@aws-cdk/aws-s3';
import * as s3notify from '@aws-cdk/aws-s3-notifications'
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
    const s3_raw_bucket = new s3.Bucket(this, 's3-raw-bucket', {
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    })
    
    const s3_proced_bucket = new s3.Bucket(this, 's3-proced-bucket', {
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    })

    /*
    const lambda_role = new iam.Role(this, "s3-hook-lambda-role", {
      assumedBy: new iam.ServicePrincipal("lambda.amazonaws.com"),
      path: "/service-role/",
      inlinePolicies: {
        S3Policy: new iam.PolicyDocument({
          statements: [
            new iam.PolicyStatement({
              actions: [
                "s3:AbortMultipartUpload",
                "s3:GetObject",
                "s3:PutObject"
              ],
              resources: ["*"]
            })
          ]
        })
      }
    });
    */
    
    // lambda triggered by s3 hook
    const s3_hook_lambda = new lambda.Function(this, 's3-hook-lambda', {
      runtime: lambda.Runtime.PYTHON_3_8,
      code: lambda.Code.fromAsset('lib/lambda/cnvFile'),
      handler: 'index.handler',
//      role: lambda_role
    });
    s3_raw_bucket.addObjectCreatedNotification(new s3notify.LambdaDestination(s3_hook_lambda))
    s3_raw_bucket.grantReadWrite(s3_hook_lambda)
    
    /*
    s3_hook_lambda.addEventSource(new lambdaES.S3EventSource(s3_raw_bucket, {
      events: [s3.EventType.OBJECT_CREATED]
    }));
    */
  }
}

