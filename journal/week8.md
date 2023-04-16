# Week 8 — Serverless Image Processing

## Required Homework 

### Implement CDK Stack

The cdk pipeline called thumbing-serverless-cdk was added to the top level directory using the command below:

```sh
cd /workspace/aws-bootcamp-cruddur-2023
mkdir thumbing-serverless-cdk
```

The CDK Stack was installed globally using the AWS CDK CLI below:

```sh
npm install aws-cdk -g
```

The install was added to my gitpod task file using the command below:

```sh
- name: cdk
  before: |
   npm install aws-cdk -g
```

### Initialize a new project

A new cdk project was initialised within the folder I created using the command below:

```sh
cdk init app --language typescript
```
      
### Thumbing Serverless CDK Stack

This script loaded environment variables, created a bucket and lambda.

```sh
import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';
import * as dotenv from 'dotenv';

//Load env variables
//const dotenv = require('dotenv')
dotenv.config();

export class ThumbingServerlessCdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here
    const bucketName: string = process.env.THUMBING_BUCKET_NAME as string;
    const folderInput: string = process.env.THUMBING_S3_FOLDER_INPUT as string;
    const folderOutput: string = process.env.THUMBING_S3_FOLDER_OUTPUT as string;
    const webhookUrl: string = process.env.THUMBING_WEBHOOK_URL as string;
    const topicName: string = process.env.THUMBING_TOPIC_NAME as string;
    const functionPath: string = process.env.THUMBING_FUNCTION_PATH as string;
    console.log('bucketName',bucketName)
    console.log('folderInput',folderInput)
    console.log('folderOutput',folderOutput)
    console.log('webhookUrl',webhookUrl)
    console.log('topicName',topicName)
    console.log('functionPath',functionPath)

    const bucket = this.createBucket(bucketName);
    const lambda = this.createLambda(functionPath, bucketName, folderInput, folderOutput);
    
  }

  createBucket(bucketName: string): s3.IBucket {
    const bucket = new s3.Bucket(this, 'ThumbingBucket', {
      bucketName: bucketName,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });
    return bucket;
  }

  createLambda(functionPath: string, bucketName: string, folderIntput: string, folderOutput: string): lambda.IFunction {
    const lambdaFunction = new lambda.Function(this, 'ThumbLambda', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'index.handler',
      code: lambda.Code.fromAsset(functionPath),
      environment: {
        DEST_BUCKET_NAME: bucketName,
        FOLDER_INPUT: folderIntput,
        FOLDER_OUTPUT: folderOutput,
        PROCESS_WIDTH: '512',
        PROCESS_HEIGHT: '512'
      }
    });
    return lambdaFunction;
  }
}
```

See screenshots below:

![S3Bucket](https://user-images.githubusercontent.com/129978840/232314987-c76e7e6b-dc1a-431a-91f7-6d9ead480b32.png)


![Lambdafunction](https://user-images.githubusercontent.com/129978840/232314997-e5c84afd-db8e-4a2a-9b46-b3aa72ead369.png)

### Synth

To run environment variable, use the command below:

```sh
npm i dotenv
```

Then cdk synth

The synth command is used to synthesize the AWS CloudFormation stack(s) that represent your infrastructure as code.

```sh
cdk synth
```

To deploy, use the command below:

```sh
cdk deploy
```

### Bootstrapping

I needed to bootstrap for region using the command below:

```sh
cdk bootstrap "aws://$AWS_ACCOUNT_ID/$AWS_DEFAULT_REGION"
```

### Addition to  Thumbing Serverless CDK Stack

#### Create SNS Topic

```sh
import * as sns from 'aws-cdk-lib/aws-sns';

const snsTopic = this.createSnsTopic(topicName)

createSnsTopic(topicName: string): sns.ITopic{
    const logicalName = "ThumbingTopic";
    const snsTopic = new sns.Topic(this, logicalName, {
      topicName: topicName
    });
    return snsTopic;
  }
```

#### Create an SNS Subscription

```sh
import * as subscriptions from 'aws-cdk-lib/aws-sns-subscriptions';

this.createSnsSubscription(snsTopic,webhookUrl)

createSnsSubscription(snsTopic: sns.ITopic, webhookUrl: string): sns.Subscription {
    const snsSubscription = snsTopic.addSubscription(
      new subscriptions.UrlSubscription(webhookUrl)
    )
    return snsSubscription;
  }
```

#### Create S3 Event Notification to SNS

```sh
this.createS3NotifyToSns(folderOutput,snsTopic,assetsBucket)

createS3NotifyToSns(prefix: string, snsTopic: sns.ITopic, bucket: s3.IBucket): void {
   const destination = new s3n.SnsDestination(snsTopic)
   bucket.addEventNotification(
      s3.EventType.OBJECT_CREATED_PUT, 
      destination,
      {prefix: prefix}
  );
}
```

#### Create S3 Event Notification to Lambda

```sh
this.createS3NotifyToLambda(folderInput,lambda,uploadsBucket)

createS3NotifyToLambda(prefix: string, lambda: lambda.IFunction, bucket: s3.IBucket): void {
    const destination = new s3n.LambdaDestination(lambda);
    bucket.addEventNotification(
      s3.EventType.OBJECT_CREATED_PUT,
      destination
  )
}
```

### Cloud Formation

The CDK was built on Cloud Formation. CloudFormation is an infrastructure automation platform for AWS that deploys AWS resources in a repeatable, testable and auditable manner.

SAM is a specialised type of CloudFormation.


### Process Images

I created a new folder called process-images within /workspace/aws-bootcamp-cruddur-2023/aws/lambdas'

```sh
cd  aws/lambdas/process-images from main directory
```

Then, ran the following command:

```sh
npm init – y
```

Install npm i sharp to process-images

```sh
npm i sharp
```

### AWS Lambda

The node_modules directory of the deployment package must include binaries for the Linux x64 platform.

When building deployment package on machines other than linux x64, run the following additional command after npm install:

```sh
npm install
rm -rf node_modules/sharp
SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install --arch=x64 --platform=linux –libc=glibc sharp
```

To remove stacks in GUI:

Run ```cdk destroy```


### Manually create s3 bucket

I manually created s3 bucket called assets.ocubeltd.co.uk


![s3bucketaddition](https://user-images.githubusercontent.com/129978840/232316688-85673ae6-8358-47ca-bfde-b481671dad42.png)

2 objects called avatars and banners were later added to this.


### Create Policy for Bucket Access

I created a policy for bucket access using the command below:

```sh
const s3ReadWritePolicy = this.createPolicyBucketAccess(bucket.bucketArn)
```

### Attach the Policies to the Lambda Role

I attached the policy to the lambda role using the command below:

```sh
lambda.addToRolePolicy(s3ReadWritePolicy);
```

### Serving Avatars via CloudFront

I created CloudFront in AWS.

See the screenshot below:

![CloudFront](https://user-images.githubusercontent.com/129978840/232319302-2dbf8a96-40bb-42e7-8ba3-3e809228064a.png)


#### Implement Avatar Uploading

I added function.rb script below to lambda and added this to the aws folder:

```sh
require 'aws-sdk-s3'
require 'json'

s3 = Aws::S3::Resource.new
bucket_name = ENV["UPLOADS_BUCKET_NAME"]
object_key = 'mock.jpg'

obj = s3.bucket(bucket_name).object(object_key)
url = obj.presigned_url(:put, expires_in: 3600)
puts url
```

I added gemfile below:

```ruby
# frozen_string_literal: true

source "https://rubygems.org"

# gem "rails"
gem "aws-sdk-s3"
gem "ox"
```

Then, ran ```bundle install``` to get gemfile.lock file.

Then, ```bundle exec ruby function.rb```

I installed ThunderClient on Github. Thunder Client is a VS Code extension for testing APIs. It is similar to Postman, but has the advantage of being able to test APIs in the same tool where code is being written.

I added a URL to thunderclient and uploaded lore.jpg, then opted for PUT.

I received a 200 message as seen below:

![ThunderClientInstall](https://user-images.githubusercontent.com/129978840/232319680-e217ff99-b20a-40e7-9495-ffb1b30f04bc.png)

This was later viewed on the S3 bucket. This loaded a mock.jpg as seen below:

![mock jpg](https://user-images.githubusercontent.com/129978840/232319849-f2a38280-59bc-4910-8e03-ba6f1e821dc4.png)

I then deleted mock.jpg from the s3 bucket.


I added the code below to Lambda:

```sh
require 'aws-sdk-s3'
require 'json'

def handler(event:, context:)
  puts event
  s3 = Aws::S3::Resource.new
  bucket_name = ENV["UPLOADS_BUCKET_NAME"]
  object_key = 'mock.jpg'

  obj = s3.bucket(bucket_name).object(object_key)
  url = obj.presigned_url(:put, expires_in: 60 * 5)
  url # this is the data that will be returned
  body = {url: url}.to_json
  { statusCode: 200, body: body }
end

puts handler(
  event: {},
  context: {}
)
```

I added the policy below to the role:

```sh
{
  "Version": "2012-10-17",
  "Statement": [
      {
          "Sid": "VisualEditor0",
          "Effect": "Allow",
          "Action": "s3:PutObject",
          "Resource": "arn:aws:s3:::ocubeltd-uploaded-avatars/*"
      }
  ]
}
```

I added the environment variable of UPLOADS_BUCKET_NAME to lambda as seen below:

![envvariable](https://user-images.githubusercontent.com/129978840/232320225-2216be7a-2a0e-4672-98ce-57376594fc4f.png)


### HTTP API Gateway with Lambda Authorizer

To get package-lock.json and package json in lambda-authorizer:

Do workspace/aws-bootcamp-cruddur-2023/aws/lambdas/lambda-authorizer -> npm install aws-jwt-verify –save

Download all the contents of lambda-authorizer and zip into a folder

Created a new lambda function called CruddurApiGatewayLambdaAuthorizer below:

![cruddurauthorizer](https://user-images.githubusercontent.com/129978840/232320436-b48e48bb-2c2f-4474-80ae-5ba9cb6d843a.png)

Uploaded the lambda-authorizer zip folder created.

I created an API Gateway using authorization, integrations & routes and also tunred on logging as seen below:

![APIAuthorization](https://user-images.githubusercontent.com/129978840/232320811-354cbfb7-8c2b-427f-9053-bed172d0bb99.png)

![APIIntegrations](https://user-images.githubusercontent.com/129978840/232320813-9b30c3ec-97de-41ff-8646-af2d8f391af1.png)

![APIRoutes](https://user-images.githubusercontent.com/129978840/232320818-56c70802-ef4a-42cb-a4cd-592bfcc321a5.png)

![Logging for api-gateway turned on](https://user-images.githubusercontent.com/129978840/232321256-86604dcc-f623-426e-b366-41a031e186f7.png)

### Cross-origin resource sharing (CORS)

Cross-origin resource sharing (CORS) defines a way for client web applications that are loaded in one domain to interact with resources in a different domain. With CORS support, you can build rich client-side web applications with Amazon S3 and selectively allow cross-origin access to your Amazon S3 resources.

S3 bucket of ocubeltd-uploaded-avatars was updated with the CORS below:

![CORS](https://user-images.githubusercontent.com/129978840/232321098-61188c87-6f52-48b2-8b4b-d6bc2502878d.png)


### Create JWT Lambda Layer

I added a layer to JWT as seen below:

![addedlayertojwt](https://user-images.githubusercontent.com/129978840/232321209-2072391c-8bf0-4ac2-9a4b-fde38dcb530a.png)

Created a custom domain to API gateway .

Run ruby-jwt command 

```ruby
./bin/lambda-layers/ruby-jwt
```

Then ```ls /tmp/```

```cd  /tmp/lambda-layers/ruby-jwt```





