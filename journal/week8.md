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
- [Serving Avatars via CloudFront](#paragraph4)
- [Updating Thumbing Serverless CDK Stack](#paragraph5)
- [Implement Users Profile Page](#paragraph6)
   - [File Creations](#subparagraph14)
   - [File Updates](#subparagraph15)
- [Implement Migrations Backend Endpoint and Profile Form](#paragraph7)
   - [File Creations](#subparagraph16)
- [Deployment Package](#paragraph8)
- [Manually create s3 bucket](#paragraph9)
- [Create Policy for Bucket Access](#paragraph10)
- [Attach the Policies to the Lambda Role](#paragraph11)
- [Implement Avatar Uploading](#paragraph12)
- [HTTP API Gateway with Lambda Authorizer](#paragraph13)
- [Cross-origin resource sharing (CORS)](#paragraph14)
- [Create JWT Lambda Layer](#paragraph15)


## Stretch Homework Challenges

## Table of contents

- [Creating a CloudFront Distribution using CloudShell](#paragraph16)
- [Disabling a CloudFront Distribution using CloudShell](#paragraph17)
- [Deleting a CloudFront Distribution using CloudShell](#paragraph18)


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

Install npm i sharp to process-images as seen below:

```sh
npm i sharp
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

### Serving Avatars via CloudFront <a name="paragraph4"></a>

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


### Updating Thumbing Serverless CDK Stack <a name="paragraph5"></a>

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


### Implement Users Profile Page <a name="paragraph6"></a>

#### File Creations <a name="subparagraph14"></a>

I created the files below for the implementation of users' profile page.

#### Edit Profile Button

This file was created within ```frontend-react-js/src/components/EditProfileButton.js``` as seen below:

import './EditProfileButton.css';

export default function EditProfileButton(props) {
  const pop_profile_form = (event) => {
    event.preventDefault();
    props.setPopped(true);
    return false;
  }

  return (
    <button onClick={pop_profile_form} className='profile-edit-button' href="#">Edit Profile</button>
  );
}

The css file was created ```frontend-react-js/src/components/EditProfileButton.css``` as seen below:

```sh
.profile-edit-button {
    border: solid 1px rgba(255,255,255,0.5);
    padding: 12px 20px;
    font-size: 18px;
    background: none;
    border-radius: 999px;
    color: rgba(255,255,255,0.8);
    cursor: pointer;
  }
  
  .profile-edit-button:hover {
    background: rgba(255,255,255,0.3)
  }
  ```

#### Profile Heading

This file was created within ```frontend-react-js/src/components/ProfileHeading.js``` as seen below:

```sh
import './ProfileHeading.css';
import EditProfileButton from '../components/EditProfileButton';

import ProfileAvatar from 'components/ProfileAvatar'

export default function ProfileHeading(props) {
  const backgroundImage = 'url("https://assets.ocubeltd.co.uk/banners/banner.jpg")';
  const styles = {
    backgroundImage: backgroundImage,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
  };
  return (
  <div className='activity_feed_heading profile_heading'>
    <div className='title'>{props.profile.display_name}</div>
    <div className="cruds_count">{props.profile.cruds_count} Cruds</div>
    <div className="banner" style={styles} >
      <ProfileAvatar id={props.profile.cognito_user_uuid} />
    </div>
    <div className="info">
      <div className='id'>
        <div className="display_name">{props.profile.display_name}</div>
        <div className="handle">@{props.profile.handle}</div>
      </div>
      <EditProfileButton setPopped={props.setPopped} />
    </div>
    <div className="bio">{props.profile.bio}</div>

  </div>
  );
}
```

The css file was created ```frontend-react-js/src/components/EditProfileButton.css``` as seen below:

```sh
.profile_heading {
  padding-bottom: 0px;
}
.profile_heading .profile-avatar {
  position: absolute;
  bottom:-74px;
  left: 16px;
  width: 148px;
  height: 148px;
  border-radius: 999px;
  border: solid 8px var(--fg);
}

.profile_heading .banner {
  position: relative;
  height: 200px;
}

.profile_heading .info {
  display: flex;
  flex-direction: row;
  align-items: start;
  padding: 16px;
}

.profile_heading .info .id {
  padding-top: 70px;
  flex-grow: 1;
}

.profile_heading .info .id .display_name {
  font-size: 24px;
  font-weight: bold;
  color: rgb(255,255,255);
}
.profile_heading .info .id .handle {
  font-size: 16px;
  color: rgba(255,255,255,0.7);
}

.profile_heading .cruds_count {
  color: rgba(255,255,255,0.7);
}

.profile_heading .bio {
  padding: 16px;
  color: rgba(255,255,255,0.7);
}
```

### Show.sql

This file was created within ```backend-flask/db/sql/users/show.sql``` as seen below:

```
SELECT 
  (SELECT COALESCE(row_to_json(object_row),'{}'::json) FROM (
    SELECT
      users.uuid,
      users.cognito_user_id as cognito_user_uuid,
      users.handle,
      users.display_name,
      users.bio,
      (
       SELECT 
        count(true) 
       FROM public.activities
       WHERE
        activities.user_uuid = users.uuid
       ) as cruds_count
  ) object_row) as profile,
  (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
    SELECT
      activities.uuid,
      users.display_name,
      users.handle,
      activities.message,
      activities.created_at,
      activities.expires_at
    FROM public.activities
    WHERE
      activities.user_uuid = users.uuid
    ORDER BY activities.created_at DESC 
    LIMIT 40
  ) array_row) as activities
FROM public.users
WHERE
  users.handle = 'AfroLatino'
```

#### File Updates <a name="subparagraph15"></a>

I updated the files below for the implementation of users' profile page.

#### User Activities

This file was updated within ```backend-flask/services/user_activities.py``` as seen below:

```sh
from lib.db import db
class UserActivities:
  def run(user_handle):
    model = {
      'errors': None,
      'data': None
    }
    if user_handle == None or len(user_handle) < 1:
      model['errors'] = ['blank_user_handle']
    else:
      print("else:")
      sql = db.template('users','show')
      results = db.query_object_json(sql,{'handle': user_handle})
      model['data'] = results
    return model
```

##### Activity Feed

This file was updated within ```frontend-react-js/src/components/ActivityFeed.js``` as seen below:

```sh
import './ActivityFeed.css';
import ActivityItem from './ActivityItem';

export default function ActivityFeed(props) {
  return (
    <div className='activity_feed_collection'>
      {props.activities.map(activity => {
      return  <ActivityItem setReplyActivity={props.setReplyActivity} setPopped={props.setPopped} key={activity.uuid} activity={activity} />
      })}
    </div>
  );
}
```

##### User Feed Page

This file was updated within ```frontend-react-js/src/components/ActivityFeed.js``` as seen below:

```sh
import {checkAuth, getAccessToken} from '../lib/CheckAuth';

export default function UserFeedPage() {
  const [activities, setActivities] = React.useState([]);
  const [profile, setProfile] = React.useState([]);
  const [popped, setPopped] = React.useState([]);
  const [poppedProfile, setPoppedProfile] = React.useState([]);
  const [user, setUser] = React.useState(null);
  const dataFetchedRef = React.useRef(false);

  const params = useParams();

  const loadData = async () => {
    try {
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/@${params.handle}`
      await getAccessToken()
      const access_token = localStorage.getItem("access_token")
      const res = await fetch(backend_url, {
        headers: {
          Authorization: `Bearer ${access_token}`
        },
        method: "GET"
      });
      let resJson = await res.json();
      if (res.status === 200) {
        console.log('setprofile',resJson.profile)
        setProfile(resJson.profile)
        setActivities(resJson.activities)
      } else {
        console.log(res)
      }
    } catch (err) {
      console.log(err);
    }
  };

  React.useEffect(()=>{
    //prevents double call
    if (dataFetchedRef.current) return;
    dataFetchedRef.current = true;

    loadData();
    checkAuth(setUser);
  }, [])

  return (
    <article>
      <DesktopNavigation user={user} active={'profile'} setPopped={setPopped} />
      <div className='content'>
        <ActivityForm popped={popped} setActivities={setActivities} />
        <ProfileForm 
          profile={profile}
          popped={poppedProfile} 
          setPopped={setPoppedProfile} 
        />
        <div className='activity_feed'>
          <ProfileHeading setPopped={setPoppedProfile} profile={profile} />
          <ActivityFeed activities={activities} />
        </div>
      </div>
      <DesktopSidebar user={user} />
    </article>
  );
}
```

Please find my screenshot of my users' page below:

![AfroLatinopics](https://user-images.githubusercontent.com/129978840/233803835-a7b6357c-706b-41a0-91f1-6c62b67ba663.jpg)


### Implement Migrations Backend Endpoint and Profile Form <a name="paragraph7"></a>

#### File Creations <a name="subparagraph16"></a>

I created the files below for the implementation of migrations backend endpoint and profile form.

#### Profile Form

This file was created within ```frontend-react-js/src/components/ActivityFeed.js``` as seen below:

```sh
import './ProfileForm.css';
import React from "react";
import process from 'process';
import {getAccessToken} from 'lib/CheckAuth';

export default function ProfileForm(props) {
  const [bio, setBio] = React.useState('');
  const [displayName, setDisplayName] = React.useState('');

  React.useEffect(()=>{
    setBio(props.profile.bio || '');
    setDisplayName(props.profile.display_name);
  }, [props.profile])

  const s3uploadkey = async (extension)=> {
    console.log('ext',extension)
    try {
      const gateway_url = `${process.env.REACT_APP_API_GATEWAY_ENDPOINT_URL}/avatars/key_upload`
      await getAccessToken()
      const access_token = localStorage.getItem("access_token")
      const json = {
        extension: extension
      }
      const res = await fetch(gateway_url, {
        method: "POST",
        body: JSON.stringify(json),
        headers: {
          'Origin': process.env.REACT_APP_FRONTEND_URL,
          'Authorization': `Bearer ${access_token}`,
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      })
      let data = await res.json();
      if (res.status === 200) {
        return data.url
      } else {
        console.log(res)
      }
    } catch (err) {
      console.log(err);
    }
  }
  const s3upload = async (event)=> {
    console.log('event',event)
    const file = event.target.files[0]
    const filename = file.name
    const size = file.size
    const type = file.type
    const preview_image_url = URL.createObjectURL(file)
    console.log(filename,size,type)
    const fileparts = filename.split('.')
    const extension = fileparts[fileparts.length-1]
    const presignedurl = await s3uploadkey(extension)
    try {
      console.log('s3upload')
      const res = await fetch(presignedurl, {
        method: "PUT",
        body: file,
        headers: {
          'Content-Type': type
      }})
      if (res.status === 200) {
        
      } else {
        console.log(res)
      }
    } catch (err) {
      console.log(err);
    }
  }

  const onsubmit = async (event) => {
    event.preventDefault();
    try {
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/profile/update`
      await getAccessToken()
      const access_token = localStorage.getItem("access_token")
      const res = await fetch(backend_url, {
        method: "POST",
        headers: {
          'Authorization': `Bearer ${access_token}`,
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          bio: bio,
          display_name: displayName
        }),
      });
      let data = await res.json();
      if (res.status === 200) {
        setBio(null)
        setDisplayName(null)
        props.setPopped(false)
      } else {
        console.log(res)
      }
    } catch (err) {
      console.log(err);
    }
  }

  const bio_onchange = (event) => {
    setBio(event.target.value);
  }

  const display_name_onchange = (event) => {
    setDisplayName(event.target.value);
  }

  const close = (event)=> {
    if (event.target.classList.contains("profile_popup")) {
      props.setPopped(false)
    }
  }

  if (props.popped === true) {
    return (
      <div className="popup_form_wrap profile_popup" onClick={close}>
        <form 
          className='profile_form popup_form'
          onSubmit={onsubmit}
        >
          <div className="popup_heading">
            <div className="popup_title">Edit Profile</div>
            <div className='submit'>
              <button type='submit'>Save</button>
            </div>
          </div>
          <div className="popup_content">
            
          <input type="file" name="avatarupload" onChange={s3upload} />

            <div className="field display_name">
              <label>Display Name</label>
              <input
                type="text"
                placeholder="Display Name"
                value={displayName}
                onChange={display_name_onchange} 
              />
            </div>
            <div className="field bio">
              <label>Bio</label>
              <textarea
                placeholder="Bio"
                value={bio}
                onChange={bio_onchange} 
              />
            </div>
          </div>
        </form>
      </div>
    );
  }
}
```

The css file was created within ```frontend-react-js/src/components/ProfileForm.css``` as follows:

```sh
.profile_popup .upload {
  color: white;
  background: green;
}
form.profile_form input[type='text'],
form.profile_form textarea {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 16px;
  border-radius: 4px;
  border: none;
  outline: none;
  display: block;
  outline: none;
  resize: none;
  width: 100%;
  padding: 16px;
  border: solid 1px var(--field-border);
  background: var(--field-bg);
  color: #fff;
}

.profile_popup .popup_content {
  padding: 16px;
}

form.profile_form .field.display_name {
  margin-bottom: 24px;
}

form.profile_form label {
  color: rgba(255,255,255,0.8);
  padding-bottom: 4px;
  display: block;
}

form.profile_form textarea {
  height: 140px;
}

form.profile_form input[type='text']:hover,
form.profile_form textarea:focus {
  border: solid 1px var(--field-border-focus)
}

.profile_popup button[type='submit'] {
  font-weight: 800;
  outline: none;
  border: none;
  border-radius: 4px;
  padding: 10px 20px;
  font-size: 16px;
  background: rgba(149,0,255,1);
  color: #fff;
}
```

#### Popup 

This file was created within ```frontend-react-js/src/components/Popup.css``` as seen below:

```sh
.popup_form_wrap {
    z-index: 100;
    position: fixed;
    height: 100%;
    width: 100%;
    top: 0;
    left: 0;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    padding-top: 48px;
    background: rgba(255,255,255,0.1)
  }
  
  .popup_form {
    background: #000;
    box-shadow: 0px 0px 6px rgba(190, 9, 190, 0.6);
    border-radius: 16px;
    width: 600px;
  }
  
  .popup_form .popup_heading {
    display: flex;
    flex-direction: row;
    border-bottom: solid 1px rgba(255,255,255,0.4);
    padding: 16px;
  }
  
  .popup_form .popup_heading .popup_title{
    flex-grow: 1;
    color: rgb(255,255,255);
    font-size: 18px;
  
  }
```

#### Update Profile

This file was created within ```backend-flask/services/update_profile.py``` as seen below:

```sh
from lib.db import db

class UpdateProfile:
  def run(cognito_user_id,bio,display_name):
    model = {
      'errors': None,
      'data': None
    }

    if display_name == None or len(display_name) < 1:
      model['errors'] = ['display_name_blank']

    if model['errors']:
      model['data'] = {
        'bio': bio,
        'display_name': display_name
      }
    else:
      handle = UpdateProfile.update_profile(bio,display_name,cognito_user_id)
      data = UpdateProfile.query_users_short(handle)
      model['data'] = data
    return model

  def update_profile(bio,display_name,cognito_user_id):
    if bio == None:    
      bio = ''

    sql = db.template('users','update')
    handle = db.query_commit(sql,{
      'cognito_user_id': cognito_user_id,
      'bio': bio,
      'display_name': display_name
    })
  def query_users_short(handle):
    sql = db.template('users','short')
    data = db.query_object_json(sql,{
      'handle': handle
    })
    return data
```

#### Update SQL

This file was created within ```backend-flask/db/sql/users/update.sql``` as seen below:

```sh
UPDATE public.users 
SET 
  bio = %(bio)s,
  display_name= %(display_name)s
WHERE 
  users.cognito_user_id = %(cognito_user_id)s
RETURNING handle;
```

App.py was also updated.


#### Migration files

A migration file was created within ```bin/generate/migration``` as seen below:

```sh
#!/usr/bin/env python3
import time
import os
import sys

if len(sys.argv) == 2:
  name = sys.argv[1]
else:
  print("pass a filename: eg. ./bin/generate/migration add_bio_column")
  exit(0)

time_now = str(int(time.time()))

filename = f"{time_now}_{name}.py"

# covert undername name to title case eg. add_bio_column -> AddBioColumn
klass = name.replace('_', ' ').title().replace(' ','')

file_content = f"""
from lib.db import db
class {klass}Migration:
  def migrate_sql():
    data = \"\"\"
    \"\"\"
    return data
  def rollback_sql():
    data = \"\"\"
    \"\"\"
    return data
  def migrate():
    db.query_commit({klass}Migration.migrate_sql(),{{
    }})
  def rollback():
    db.query_commit({klass}Migration.rollback_sql(),{{
    }})
migration = AddBioColumnMigration
"""
#remove leading and trailing new lines
file_content = file_content.lstrip('\n').rstrip('\n')

current_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.abspath(os.path.join(current_path, '..', '..','backend-flask','db','migrations',filename))
print(file_path)

with open(file_path, 'w') as f:
  f.write(file_content)
```

Make this executable by running ```chmod u+x ./bin/generate/migration add_bio_column```

Run this command ```./bin/generate/migration add_bio_column``` to generate a migration file within ```backend-flask/db/migrations``` as seen below:

```sh
from lib.db import db
class AddBioColumnMigration:
  def migrate_sql():
    data = """
    ALTER TABLE public.users ADD COLUMN bio text;
    """
    return data
  def rollback_sql():
    data = """
    ALTER TABLE public.users DROP COLUMN bio;
    """
    return data
  def migrate():
    db.query_commit(AddBioColumnMigration.migrate_sql(),{
    })
  def rollback():
    db.query_commit(AddBioColumnMigration.rollback_sql(),{
    })
migration = AddBioColumnMigration
```

```ALTER TABLE public.users ADD COLUMN bio text``` was added to migrate_sql command and ```ALTER TABLE public.users DROP COLUMN bio``` was added to rollback sql command.
  
A ```.keep``` file was also added to this directory. This is left blank.

A migrate file was created within ```bin/db/migrate```

This is for migrating changes.

```sh
#!/usr/bin/env python3

import os
import sys
import glob
import re
import time
import importlib

current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, '..', '..','backend-flask'))
sys.path.append(parent_path)
from lib.db import db

def get_last_successful_run():
  sql = """
    SELECT last_successful_run
    FROM public.schema_information
    LIMIT 1
  """
  return int(db.query_value(sql,{},verbose=False))

def set_last_successful_run(value):
  sql = """
  UPDATE schema_information
  SET last_successful_run = %(last_successful_run)s
  WHERE id = 1
  """
  db.query_commit(sql,{'last_successful_run': value},verbose=False)
  return value

last_successful_run = get_last_successful_run()

migrations_path = os.path.abspath(os.path.join(current_path, '..', '..','backend-flask','db','migrations'))
sys.path.append(migrations_path)
migration_files = glob.glob(f"{migrations_path}/*")


for migration_file in migration_files:
  filename = os.path.basename(migration_file)
  module_name = os.path.splitext(filename)[0]
  match = re.match(r'^\d+', filename)
  if match:
    file_time = int(match.group())
    if last_successful_run <= file_time:
      mod = importlib.import_module(module_name)
      print('=== running migration: ',module_name)
      mod.migration.migrate()
      time_now = str(int(time.time()))
      last_successful_run = set_last_successful_run(time_now)
```

A rollback file was created within ```bin/db/rollback``` as follows:

```sh
#!/usr/bin/env python3

import os
import sys
import glob
import re
import time
import importlib

current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, '..', '..','backend-flask'))
sys.path.append(parent_path)
from lib.db import db

def get_last_successful_run():
  sql = """
    SELECT last_successful_run
    FROM public.schema_information
    LIMIT 1
  """
  return int(db.query_value(sql,{},verbose=False))

def set_last_successful_run(value):
  sql = """
  UPDATE schema_information
  SET last_successful_run = %(last_successful_run)s
  WHERE id = 1
  """
  db.query_commit(sql,{'last_successful_run': value})
  return value

last_successful_run = get_last_successful_run()

migrations_path = os.path.abspath(os.path.join(current_path, '..', '..','backend-flask','db','migrations'))
sys.path.append(migrations_path)
migration_files = glob.glob(f"{migrations_path}/*")


last_migration_file = None
for migration_file in migration_files:
  if last_migration_file == None:
    filename = os.path.basename(migration_file)
    module_name = os.path.splitext(filename)[0]
    match = re.match(r'^\d+', filename)
    if match:
      file_time = int(match.group())
      print("==<><>")
      print(last_successful_run, file_time)
      print(last_successful_run > file_time)
      if last_successful_run > file_time:
        last_migration_file = module_name
        mod = importlib.import_module(module_name)
        print('=== rolling back: ',module_name)
        mod.migration.rollback()
        set_last_successful_run(file_time)
```

The rollback file was for rolling back changes if needed.

```backend-flask/db/schema.sql``` was updated with ```public.schema_information``` as seen below:

```sh
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.activities;

CREATE TABLE IF NOT EXISTS public.schema_information (
  id integer UNIQUE,
  last_successful_run text
);
INSERT INTO public.schema_information (id, last_successful_run)
VALUES(1, '0')
ON CONFLICT (id) DO NOTHING;


CREATE TABLE public.users (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  display_name text NOT NULL,
  handle text NOT NULL,
  email text NOT NULL,
  cognito_user_id text NOT NULL,
  created_at TIMESTAMP default current_timestamp NOT NULL
);

CREATE TABLE public.activities (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_uuid UUID NOT NULL,
  message text NOT NULL,
  replies_count integer DEFAULT 0,
  reposts_count integer DEFAULT 0,
  likes_count integer DEFAULT 0,
  reply_to_activity_uuid integer,
  expires_at TIMESTAMP,
  created_at TIMESTAMP default current_timestamp NOT NULL
);
```

### Deployment Package <a name="paragraph8"></a>

The node_modules directory of the deployment package must include binaries for the Linux x64 platform.

When building deployment package on machines other than linux x64, run the following additional command after npm install:

```sh
npm install
rm -rf node_modules/sharp
SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install --arch=x64 --platform=linux –libc=glibc sharp
```

To remove stacks in GUI:

Run ```cdk destroy```


### Manually create s3 bucket <a name="paragraph9"></a>

I manually created s3 bucket called assets.ocubeltd.co.uk

![s3bucketaddition](https://user-images.githubusercontent.com/129978840/232316688-85673ae6-8358-47ca-bfde-b481671dad42.png)

2 objects called avatars and banners were later added to this.


### Create Policy for Bucket Access <a name="paragraph10"></a>

I created a policy for bucket access using the command below:

```sh
const s3ReadWritePolicy = this.createPolicyBucketAccess(bucket.bucketArn)
```

### Attach the Policies to the Lambda Role <a name="paragraph11"></a>

I attached the policy to the lambda role using the command below:

```sh
lambda.addToRolePolicy(s3ReadWritePolicy);
```

#### Implement Avatar Uploading <a name="paragraph12"></a>

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


### HTTP API Gateway with Lambda Authorizer <a name="paragraph13"></a>

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


### Cross-origin resource sharing (CORS) <a name="paragraph14"></a>

Cross-origin resource sharing (CORS) defines a way for client web applications that are loaded in one domain to interact with resources in a different domain. With CORS support, you can build rich client-side web applications with Amazon S3 and selectively allow cross-origin access to your Amazon S3 resources.

S3 bucket of ocubeltd-uploaded-avatars was updated with the CORS below:

![CORS](https://user-images.githubusercontent.com/129978840/232321098-61188c87-6f52-48b2-8b4b-d6bc2502878d.png)


### Create JWT Lambda Layer <a name="paragraph15"></a>

I added a layer to JWT as seen below:

![addedlayertojwt](https://user-images.githubusercontent.com/129978840/232321209-2072391c-8bf0-4ac2-9a4b-fde38dcb530a.png)

Created a custom domain to API gateway .

Run ruby-jwt command 

```ruby
./bin/lambda-layers/ruby-jwt
```

Then ```ls /tmp/```

```cd  /tmp/lambda-layers/ruby-jwt```



## Stretch Homework Challenges

### Creating a CloudFront Distribution using CloudShell <a name="paragraph16"></a>

The example below creates a distribution for an S3 bucket named **afrolatino.s3.amazonaws.com**, and also specifies index.html as the default root object, using command line arguments:

```sh
aws cloudfront create-distribution \
    --origin-domain-name afrolatino.s3.amazonaws.com \
    --cli-read-timeout 30 \
    --cli-connect-timeout 30 \
    --default-root-object index.html
```

#### cli-read-timeout (int)

The maximum socket read time in seconds. If the value is set to 0, the socket read will be blocking and not timeout. The default value is 60 seconds.

#### cli-connect-timeout (int)

The maximum socket connect time in seconds. If the value is set to 0, the socket connect will be blocking and not timeout. The default value is 60 seconds.

Please find below the screenshot of the distribution created:

![newdistribution](https://user-images.githubusercontent.com/78261965/234663785-439a8a11-b323-4551-b829-ed73472dae12.png)


### Disabling a CloudFront Distribution using CloudShell <a name="paragraph17"></a>

Before you can delete a distribution, you must disable it, which requires permission to update the distribution.

The following example disables the CloudFront distribution with the ID E1QWQFTW851VU by providing the distribution configuration in a JSON file named dist-config-disable.json. To update a distribution, you must use the --if-match option to provide the distribution's ETag. To get the ETag, use the get-distribution or get-distribution-config command.

After you use the following example to disable a distribution, you can use the delete-distribution command to delete it.


aws cloudfront update-distribution --id E1QWQFTW851VU \
    --default-root-object index.html

  
### Getting the ETag of the distribution

To delete a distribution, you must use the --if-match option to provide the distribution's ETag. 

The example below extracts the ETag of the CloudFront distribution with the ID E1QWQFTW851VU. 

```sh
aws cloudfront get-distribution --id E1QWQFTW851VU
```

Please find below the screenshot of the query:

![Etag](https://user-images.githubusercontent.com/78261965/234665875-beee1db6-5e3b-4bc5-a1d1-a04e2d2d2a3c.png)


### Deleting a CloudFront Distribution using CloudShell <a name="paragraph18"></a>

The following example deletes the CloudFront distribution with the ID E1QWQFTW851VU. Before you can delete a distribution, you must disable it. 

You can do this through the Management Console or CLI command using the below:

```sh
aws cloudfront update-distribution \
    --id EMLARXS9EXAMPLE \
    --if-match E2QWRUHEXAMPLE \
    --distribution-config file://dist-config-disable.json
```

Please find bwlo the disabled distribution:

![disabled](https://user-images.githubusercontent.com/78261965/234672669-5fa7aa9a-1af6-4c06-be1c-c1b3d041f05b.png)

When a distribution is disabled, you can delete it. To delete a distribution, you must use the --if-match option to provide the distribution's ETag. To get the ETag, use the get-distribution or get-distribution-config command.

To get a CloudFront distribution



Then delete the distribution using the command below:

aws cloudfront delete-distribution \
    --id E1QWQFTW851VU \
    --if-match E1HHDOGRIDL61M
    
When successful, this command has no output. 



