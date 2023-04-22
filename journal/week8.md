# Week 8 — Serverless Image Processing

## Required Homework 

## Table of contents

- [Introduction](#introduction)
- [Implement CDK Stack](#paragraph1)
   - [Initialize a new project](#subparagraph1)
   - [Thumbing Serverless CDK Stack](#subparagraph2)
   - [Synth](#subparagraph3)
   - [Deploy](#subparagraph4)
   - [Bootstrapping](#subparagraph5)
- [Lambda Codes](#paragraph2)
   - [Lambda code for Processing Images](#subparagraph6)
   - [Lambda code for Testing Processing Images](#subparagraph7)
   - [Lambda code for Image Processing using S3](#subparagraph8)
   - [Lambda code for example JSON file for Processing Images](#subparagraph9)
- [Additional creations to Thumbing Serverless CDK Stack](#paragraph3)
   - [Create SNS Topic](#subparagraph10)
   - [Create an SNS Subscription](#subparagraph11)
   - [Create S3 Event Notification to SNS](#subparagraph12)
   - [Create S3 Event Notification to Lambda](#subparagraph13)
- [Served Avatars via CloudFront](#paragraph4)
 

### Introduction <a name="introduction"></a>

AWS CDK lets you build reliable, scalable, cost-effective applications in the cloud with the considerable expressive power of a programming language. 

It uses the power of AWS CloudFormation to perform infrastructure deployments predictably and repeatedly, with rollback on error.


### Implement CDK Stack <a name="paragraph1"></a>

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

#### Initialize a new project <a name="subparagraph1"></a>

A new cdk project was initialised within the folder I created using the command below:

```sh
cdk init app --language typescript
```
      
#### Thumbing Serverless CDK Stack <a name="subparagraph2"></a>

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

The environment variables were loaded in the ```.env.example``` file as seen below:

```sh
THUMBING_BUCKET_NAME="ocubeltd-uploaded-avatars"
THUMBING_S3_FOLDER_INPUT="avatars/original/"
THUMBING_S3_FOLDER_OUTPUT="avatars/processed"
THUMBING_WEBHOOK_URL="https://api.ocubeltd.co.uk/webhooks/avatar"
THUMBING_TOPIC_NAME="cruddur-assets"
THUMBING_FUNCTION_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/lambdas/process-images"
```

To run environment variable, use the command below:

```sh
npm i dotenv
```

#### Synth <a name="subparagraph3"></a>

The synth command is used to synthesize the AWS CloudFormation stack(s) that represent your infrastructure as code.

```sh
cdk synth
```

#### Deploy <a name="subparagraph4"></a>

To deploy, use the command below:

```sh
cdk deploy
```

See screenshots below:

![S3Bucket](https://user-images.githubusercontent.com/129978840/232314987-c76e7e6b-dc1a-431a-91f7-6d9ead480b32.png)


#### Bootstrapping <a name="subparagraph5"></a>

I needed to bootstrap for region using the command below:

```sh
cdk bootstrap "aws://$AWS_ACCOUNT_ID/$AWS_DEFAULT_REGION"
```


### Lambda codes <a name="paragraph2"></a>

#### Lambda code for Processing Images <a name="subparagraph6"></a>

The lambda code below was created for processing images.

This is available via ```aws/lambdas/process-images/index.js```

```sh
const process = require('process');
const {getClient, getOriginalImage, processImage, uploadProcessedImage} = require('./s3-image-processing.js')
const path = require('path');

const bucketName = process.env.DEST_BUCKET_NAME
const folderInput = process.env.FOLDER_INPUT
const folderOutput = process.env.FOLDER_OUTPUT
const width = parseInt(process.env.PROCESS_WIDTH)
const height = parseInt(process.env.PROCESS_HEIGHT)

client = getClient();

exports.handler = async (event) => {
  const srcBucket = event.Records[0].s3.bucket.name;
  const srcKey = decodeURIComponent(event.Records[0].s3.object.key.replace(/\+/g, ' '));
  console.log('srcBucket',srcBucket)
  console.log('srcKey',srcKey)

  const dstBucket = bucketName;

  filename = path.parse(srcKey).name
  const dstKey = `${folderOutput}/${filename}.jpg`
  console.log('dstBucket',dstBucket)
  console.log('dstKey',dstKey)

  const originalImage = await getOriginalImage(client,srcBucket,srcKey)
  const processedImage = await processImage(originalImage,width,height)
  await uploadProcessedImage(client,dstBucket,dstKey,processedImage)
};
```

See the screenshot below of the lambda function:

![Lambdafunction](https://user-images.githubusercontent.com/129978840/232314997-e5c84afd-db8e-4a2a-9b46-b3aa72ead369.png)


#### Lambda code for Testing Processing Images <a name="subparagraph7"></a>

The lambda code below was created for testing processing images.

This is available via ```aws/lambdas/process-images/test.js```

```sh
const {getClient, getOriginalImage, processImage, uploadProcessedImage} = require('./s3-image-processing.js')

async function main(){
  client = getClient()
  const srcBucket = 'cruddur-thumbs'
  const srcKey = 'avatar/original/data.jpg'
  const dstBucket = 'cruddur-thumbs'
  const dstKey = 'avatar/processed/data.png'
  const width = 256
  const height = 256

  const originalImage = await getOriginalImage(client,srcBucket,srcKey)
  console.log(originalImage)
  const processedImage = await processImage(originalImage,width,height)
  await uploadProcessedImage(client,dstBucket,dstKey,processedImage)
}

main()
```

#### Lambda code for Image Processing using S3 <a name="subparagraph8"></a>

The lambda code below was created for image processing using s3.

This is available via ```aws/lambdas/process-images/s3-image-processing-file.js```

```sh
const sharp = require('sharp');
const { S3Client, PutObjectCommand, GetObjectCommand } = require("@aws-sdk/client-s3");

function getClient(){
  const client = new S3Client();
  return client;
}

async function getOriginalImage(client,srcBucket,srcKey){
  console.log('get==')
  const params = {
    Bucket: srcBucket,
    Key: srcKey
  };
  console.log('params',params)
  const command = new GetObjectCommand(params);
  const response = await client.send(command);

  const chunks = [];
  for await (const chunk of response.Body) {
    chunks.push(chunk);
  }
  const buffer = Buffer.concat(chunks);
  return buffer;
}

async function processImage(image,width,height){
  const processedImage = await sharp(image)
    .resize(width, height)
    .jpeg()
    .toBuffer();
  return processedImage;
}

async function uploadProcessedImage(client,dstBucket,dstKey,image){
  console.log('upload==')
  const params = {
    Bucket: dstBucket,
    Key: dstKey,
    Body: image,
    ContentType: 'image/jpeg'
  };
  console.log('params',params)
  const command = new PutObjectCommand(params);
  const response = await client.send(command);
  console.log('repsonse',response);
  return response;
}

module.exports = {
  getClient: getClient,
  getOriginalImage: getOriginalImage,
  processImage: processImage,
  uploadProcessedImage: uploadProcessedImage
}
```

This was installed using the command below:

```sh
npm i sharp @aws-sdk/client-s3
```

#### Lambda code for example JSON file for Processing Images <a name="subparagraph9"></a>

The lambda code below was created as an example JSON file for processing images.

This is available via ```aws/lambdas/process-images/example.json```

```sh
{
    "Records": [
      {
        "eventVersion": "2.0",
        "eventSource": "aws:s3",
        "awsRegion": "us-east-1",
        "eventTime": "1970-01-01T00:00:00.000Z",
        "eventName": "ObjectCreated:Put",
        "userIdentity": {
          "principalId": "EXAMPLE"
        },
        "requestParameters": {
          "sourceIPAddress": "127.0.0.1"
        },
        "responseElements": {
          "x-amz-request-id": "EXAMPLE123456789",
          "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
        },
        "s3": {
          "s3SchemaVersion": "1.0",
          "configurationId": "testConfigRule",
          "bucket": {
            "name": "assets.ocubeltd.co.uk",
            "ownerIdentity": {
              "principalId": "EXAMPLE"
            },
            "arn": "arn:aws:s3:::assets.ocubeltd.co.uk"
          },
          "object": {
            "key": "avatars/original/data.jpg",
            "size": 1024,
            "eTag": "0123456789abcdef0123456789abcdef",
            "sequencer": "0A1B2C3D4E5F678901"
          }
        }
      }
    ]
  }
```
  
### Additional creations to Thumbing Serverless CDK Stack <a name="paragraph3"></a>

#### Create SNS Topic <a name="subparagraph10"></a>

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

#### Create an SNS Subscription <a name="subparagraph11"></a>

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

#### Create S3 Event Notification to SNS <a name="subparagraph12"></a>

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

#### Create S3 Event Notification to Lambda <a name="subparagraph13"></a>

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

### Served Avatars via CloudFront <a name="paragraph4"></a>

Amazon CloudFront is a web service that gives businesses and web application developers an easy and cost effective way to distribute content with low latency and high data transfer speeds.

Find below the steps for creating a distribution in CloiudFront:

- Search for CloudFront amongst AWS Services. Then, navigate to the screen and click on **Create distribution**
- For **Origin domain**, choose the name with a prefix of *assets* under *Amazon S3*. This automatically populates the **Origin Name**
- Select **Origin access control settings (recommended)** as **Origin access**
- Select **Create control setting**. This automatically populates **Origin access control**
- Leave the default settings for **Enable Origin Shield** and **Default cache behavior**
- Under **Viewer protocol policy**, choose **Redirect HTTP to HTTPS** and default setting for **Allowed HTTP methods**
- Under **Cache key and origin requests**, leave the default setting of **Cache policy and origin request policy (recommended)** and **Cache policy** of **CacheOptimized** recommended for S3.
- Select **CORS-CustomOrigin** as the **Origin request policy**
- For **Settings**, leave the default setting of **Price class**
- Enter **Alternate domain name (CNAME)** as **assets.<domain_name>**
- Select the public certificate created as **Custom SSL certificate**
- Leave the default settings of **Supported HTTP versions**, **Standard logging** and **IPv6**
- I added a description to **Description - optional** section
- Then, click on **Create distribution**

See the screenshot below of the distribution created in CloudFront:

![CloudFront](https://user-images.githubusercontent.com/129978840/232319302-2dbf8a96-40bb-42e7-8ba3-3e809228064a.png)


### Updating Thumbing Serverless CDK Stack

THUMBING_BUCKET_NAME & THUMBING_S3_FOLDER_INPUT environment variables created within ```thumbing-serverless-cdk/.env.example``` file were updated to UPLOADS_BUCKET_NAME & ASSETS_BUCKET_NAME as seen below:

```sh
UPLOADS_BUCKET_NAME="ocubeltd-uploaded-avatars"
ASSETS_BUCKET_NAME="assets.ocubeltd.co.uk"
```

Then, ```thumbing-serverless-cdk-stack.ts``` was updated as follows:

```sh
export class ThumbingServerlessCdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here
    const uploadsBucketName: string = process.env.UPLOADS_BUCKET_NAME as string;
    const assetsBucketName: string = process.env.ASSETS_BUCKET_NAME as string;
    const folderInput: string = process.env.THUMBING_S3_FOLDER_INPUT as string;
    const folderOutput: string = process.env.THUMBING_S3_FOLDER_OUTPUT as string;
    const webhookUrl: string = process.env.THUMBING_WEBHOOK_URL as string;
    const topicName: string = process.env.THUMBING_TOPIC_NAME as string;
    const functionPath: string = process.env.THUMBING_FUNCTION_PATH as string;
    console.log('uploadsBucketName',)
    console.log('assetsBucketName',assetsBucketName)
    console.log('folderInput',folderInput)
    console.log('folderOutput',folderOutput)
    console.log('webhookUrl',webhookUrl)
    console.log('topicName',topicName)
    console.log('functionPath',functionPath)

    const uploadsBucket = this.createBucket(uploadsBucketName);
    const assetsBucket = this.importBucket(assetsBucketName);
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





