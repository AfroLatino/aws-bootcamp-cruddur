# Week X — Tidying up the codes

## Table of contents
- [Introduction](#introduction)
- [Sync tool for static website hosting](#paragraph1)
- [Reconnect Database and Post Confirmation Lambda](#paragraph2)
- [Use CORS for Service](#paragraph3)
- [CICD Pipeline and Create Activity](#paragraph4)
- [Refactor JWT to use a decorator](#paragraph5)
- [Refactor AppPy](#paragraph6)
- [Refactor Flask Routes](#paragraph7)
- [Replies Work In Progress](#paragraph8)
- [Refactor Error Handling and Fetch Requests](#paragraph9)
- [Activity Show Page](#paragraph10)


### Introduction  <a name="introduction"></a>

This was the final week of cleaning up all the codes from the app to make them more readable and efficient.


### Sync tool for static website hosting <a name="paragraph1"></a>

Create a new file called ```static-build``` within bin / frontend folder with the command below:

```sh
#! /usr/bin/bash

ABS_PATH=$(readlink -f "$0")
FRONTEND_PATH=$(dirname $ABS_PATH)
BIN_PATH=$(dirname $FRONTEND_PATH)
PROJECT_PATH=$(dirname $BIN_PATH)
FRONTEND_REACT_JS_PATH="$PROJECT_PATH/frontend-react-js"

cd $FRONTEND_REACT_JS_PATH

REACT_APP_BACKEND_URL="https://api.ocubeltd.co.uk" \
REACT_APP_AWS_PROJECT_REGION="$AWS_DEFAULT_REGION" \
REACT_APP_AWS_COGNITO_REGION="$AWS_DEFAULT_REGION" \
REACT_APP_AWS_USER_POOLS_ID="$AWS_COGNITO_AWS_USER_POOL_ID" \
REACT_APP_CLIENT_ID="$AWS_COGNITO_AWS_USER_POOL_CLIENT_ID" \
npm run build
```

Amend ```frontend-react-js/src/pages/SigninPage.js``` with parts of the command below:

```sh
const onsubmit = async (event) => {
    setErrors('')
    event.preventDefault();
    Auth.signIn(email, password)
    .then(user => {
      console.log('user',user)
      localStorage.setItem("access_token", user.signInUserSession.accessToken.jwtToken)
      window.location.href = "/"
    })
    .catch(error => { 
      if (error.code === 'UserNotConfirmedException') {
        window.location.href = "/confirm"
      }
      setErrors(error.message)
    });
    return false
  }
```

Amend ```frontend-react-js/src/components/ActivityContent.css``` by adding flex-start to align-items with parts of the command below:

```sh
.activity_content_wrap {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
}
```

Amend ```frontend-react-js/src/pages/RecoverPage.js``` with parts of the command below:

```sh
const onsubmit_confirm_code = async (event) => {
    event.preventDefault();
    setErrors('')
    if (password === passwordAgain){
      Auth.forgotPasswordSubmit(username, code, password)
      .then((data) => setFormState('success'))
      .catch((err) => setErrors(err.message) );
    } else {
      setErrors('Passwords do not match')
    }
    return false
  }
  
  ---
  
  let form;
  if (formState === 'send_code') {
    form = send_code()
  }
  else if (formState === 'confirm_code') {
    form = confirm_code()
  }
  else if (formState === 'success') {
    form = success()
  }
```

Amend ```frontend-react-js/src/pages/ConfirmationPage.js``` with parts of the command below:

```sh
const resend_code = async (event) => {
    setErrors('')
    try {
      await Auth.resendSignUp(email);
      console.log('code resent successfully');
      setCodeSent(true)
    } catch (err) {
      // does not return a code
      // does cognito always return english
      // for this to be an okay match?
      console.log(err)
      if (err.message === 'Username cannot be empty'){
        setErrors("You need to provide an email in order to send Resend Activiation Code")   
      } else if (err.message === "Username/client id combination not found."){
        setErrors("Email is invalid or cannot be found.")   
      }
    }
  }
```

Amend ```frontend-react-js/src/components/ProfileInfo.js``` with parts of the command below:

```sh
const classes = () => {
    let classes = ["profile-info-wrapper"];
    if (popped === true){
      classes.push('popped');
    }
    return classes.join(' ');
  }
```

Amend ```frontend-react-js/src/components/ProfileForm.js``` with parts of the command below:

```sh
let data = await res.json();
      if (res.status === 200) {
        return data.url
      } else {
        console.log(res)
      }
    } catch (err) {
      console.log(err);
 ```

Comment out codes not being used as follows:

```sh
//let data = await res.json();

--

//const preview_image_url = URL.createObjectURL(file)
```

Amend ```frontend-react-js/src/components/MessageGroupItem.js``` with parts of the command below:

```sh
  const classes = () => {
    let classes = ["message_group_item"];
    if (params.message_group_uuid === props.message_group.uuid){
      classes.push('active')
    }
    return classes.join(' ');
  }
 ```
 
 Amend ```frontend-react-js/src/components/MessageForm.js``` by adding the code below:
 
 ```sh
 import { useParams } from 'react-router-dom';
 ```
 
 Amend ```frontend-react-js/src/components/DesktopSidebar.js``` with parts of the command below:
 
 ```sh
   return (
    <section>
      <Search />
      {trending}
      {suggested}
      {join}
      <footer>
        <a href="/about">About!</a>
        <a href="/terms-of-service">Terms of Service</a>
        <a href="/privacy-policy">Privacy Policy</a>
      </footer>
    </section>
  );
}
```

Amend ```frontend-react-js/src/components/DesktopNavigationLink.js``` with parts of the command below:

```sh
 const icon = ()=> {
    switch(props.handle){
      case 'home':
        return <HomeIcon className='icon' />
        break;
      case 'notifications':
        return <NotificationsIcon className='icon' />
        break;
      case 'profile':
        return <ProfileIcon className='icon' />
        break;
      case 'more':
        return <MoreIcon className='icon' />
        break;
      case 'messages':
        return <MessagesIcon className='icon' />
        break;
      default: 
        break;
    }
  }
```

Amend ```frontend-react-js/src/components/MessageGroupItem.css``` with parts of the command below:

```sh
.message_group_item {
  display: flex;
  align-items: flex-start;
  overflow: hidden;
  padding: 16px;
  cursor: pointer;
  text-decoration: none;
}
```

Amend ```frontend-react-js/src/components/MessageItem.css``` with parts of the command below:

```sh
.message_item {
  display: flex;
  align-items: flex-start;
  overflow: hidden;
  border-bottom: solid 1px rgb(31,36,49);
  padding: 16px;
  cursor: pointer;
  text-decoration: none;
}
```

Amend ```frontend-react-js/src/components/ProfileHeading.css``` with parts of the command below:

```sh
.profile_heading .info {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  padding: 16px;
}
```

Amend ```frontend-react-js/src/components/MessageGroupItem.js``` with parts of the command below:

```sh
const classes = () => {
    let classes = ["message_group_item"];
    if (params.message_group_uuid === props.message_group.uuid){
      classes.push('active')
    }
    return classes.join(' ');
  }
```

Run the command below in the frontend-flask directory; ```/workspace/aws-bootcamp-cruddur-2023/frontend-react-js``` to build the application:

```sh
REACT_APP_BACKEND_URL="https://api.ocubeltd.co.uk" \
REACT_APP_AWS_PROJECT_REGION="$AWS_DEFAULT_REGION" \
REACT_APP_AWS_COGNITO_REGION="$AWS_DEFAULT_REGION" \
REACT_APP_AWS_USER_POOLS_ID="$AWS_USER_POOLS_ID" \
REACT_APP_CLIENT_ID="$APP_CLIENT_ID" \
npm run build
```

Zip the contents by running the command below:

```sh
zip -r build.zip build/
```

- This creates the build.zip file
- Right click and download the file
- Delete the build.zip file from the directory.
- Navigate to Amazon S3 -> Buckets -> ocubeltd.co.uk
- Copy the build zip folder onto the desktop
- Open the build folder
- Copy and drag all the contents onto the page
- Click on upload

I typed ocubeltd.co.uk on the URL and got the web application as seen below:

![ocubeltd co uk_webapplication_showing](https://github.com/AfroLatino/aws-bootcamp-cruddur-2023/assets/78261965/b8ccfb18-bb04-4b07-bd28-13d19762ea43)

Create a file called ```sync``` within ```bin / frontend``` directory with the command below:

```sh
#!/usr/bin/env ruby

require 'aws_s3_website_sync'
require 'dotenv'

env_path = "/workspace/aws-bootcamp-cruddur-2023/sync.env"
Dotenv.load(env_path)

puts "== configuration"
puts "aws_default_region:   #{ENV["AWS_DEFAULT_REGION"]}"
puts "s3_bucket:            #{ENV["SYNC_S3_BUCKET"]}"
puts "distribution_id:      #{ENV["SYNC_CLOUDFRONT_DISTRUBTION_ID"]}"
puts "build_dir:            #{ENV["SYNC_BUILD_DIR"]}"

changeset_path = ENV["SYNC_OUTPUT_CHANGESET_PATH"]
changeset_path = changeset_path.sub(".json","-#{Time.now.to_i}.json")

puts "output_changset_path: #{changeset_path}"
puts "auto_approve:         #{ENV["SYNC_AUTO_APPROVE"]}"

puts "sync =="
AwsS3WebsiteSync::Runner.run(
  aws_access_key_id:     ENV["AWS_ACCESS_KEY_ID"],
  aws_secret_access_key: ENV["AWS_SECRET_ACCESS_KEY"],
  aws_default_region:    ENV["AWS_DEFAULT_REGION"],
  s3_bucket:             ENV["SYNC_S3_BUCKET"],
  distribution_id:       ENV["SYNC_CLOUDFRONT_DISTRUBTION_ID"],
  build_dir:             ENV["SYNC_BUILD_DIR"],
  output_changset_path:  changeset_path,
  auto_approve:          ENV["SYNC_AUTO_APPROVE"],
  silent: "ignore,no_change",
  ignore_files: [
    'stylesheets/index',
    'android-chrome-192x192.png',
    'android-chrome-256x256.png',
    'apple-touch-icon-precomposed.png',
    'apple-touch-icon.png',
    'site.webmanifest',
    'error.html',
    'favicon-16x16.png',
    'favicon-32x32.png',
    'favicon.ico',
    'robots.txt',
    'safari-pinned-tab.svg'
  ]
)
```

In the main directory, install gem by running the command below:

```sh
gem install aws_s3_website_sync
```

Create a new file within ```erb``` in the main directory called ```sync.env.erb``` with the command below:

```sh
SYNC_S3_BUCKET=$SYNC_S3_BUCKET
SYNC_CLOUDFRONT_DISTRIBUTION_ID=$SYNC_CLOUDFRONT_DISTRIBUTION_ID 
// This is the distribution ID for Frontend React JS for Cruddur
SYNC_BUILD_DIR=<%= ENV['THEIA_WORKSPACE_ROOT'] %>/frontend-react-js/build
SYNC_OUTPUT_CHANGESET_PATH=<%=  ENV['THEIA_WORKSPACE_ROOT'] %>/tmp
SYNC_AUTO_APPROVE=false
```

Amend ```bin/ frontend/ generate-env``` as follows:

```sh
#!/usr/bin/env ruby

require 'erb'

template = File.read 'erb/frontend-react-js.env.erb'
content = ERB.new(template).result(binding)
filename = "frontend-react-js.env"
File.write(filename, content)

template = File.read 'erb/sync.env.erb'
content = ERB.new(template).result(binding)
filename = "sync.env"
File.write(filename, content)
```

Gem install env by using the command below:

```sh
gem install dotenv
```

Make sync file executable by running ```chmod u+x ./bin/frontend/sync```

Then run ```./bin/frontend/sync```

Create a ```tmp``` folder in the main directory and add a file called ```.keep```


#### Adding github actions

Create a folder called ```github```, then another folder inside github called ```workflows```, then a file called ```sync.yaml.example``` with the command below:

```sh
name: Sync-Prod-Frontend

on:
  push:
    branches: [ prod ]
  pull_request:
    branches: [ prod ]

jobs:
  build:
    name: Statically Build Files
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [ 18.x]
    steps:
      - uses: actions/checkout@v3
      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
      - run: cd frontend-react-js
      - run: npm ci
      - run: npm run build
  deploy:
    name: Sync Static Build to S3 Bucket
    runs-on: ubuntu-latest
    # These permissions are needed to interact with GitHub's OIDC Token endpoint.
    permissions:
      id-token: write
      contents: read
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Configure AWS credentials from Test account
        uses: aws-actions/configure-aws-credentials@v2
        with:
          role-to-assume: arn:aws:iam::$AWS_ACCOUNT_ID:role/CrdSyncRole-Role-1N0SLA7KGVS8E
          aws-region: $AWS_DEFAULT_REGION
      - uses: actions/checkout@v3
      - name: Set up Ruby
        uses: ruby/setup-ruby@ec02537da5712d66d4d50a0f33b7eb52773b5ed1
        with:
          ruby-version: '3.1'
      - name: Install dependencies
        run: bundle install
      - name: Run tests
        run: bundle exec rake sync
```

Create a new file called ```Gemfile``` in the main directory with the command below:

```sh
source 'https://rubygems.org'

git_source(:github) do |repo_name|
  repo_name = "#{repo_name}/#{repo_name}" unless repo_name.include?("/")
  "https://github.com/#{repo_name}.git"
end

gem 'rake'
gem 'aws_s3_website_sync', tag: '1.0.1'
gem 'dotenv', groups: [:development, :test]
```

Create a new file called Rakefile in the main directory with the command below:

```sh
require 'aws_s3_website_sync'
require 'dotenv'

task :sync do
  puts "sync =="
  AwsS3WebsiteSync::Runner.run(
    aws_access_key_id:     ENV["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key: ENV["AWS_SECRET_ACCESS_KEY"],
    aws_default_region:    ENV["AWS_DEFAULT_REGION"],
    s3_bucket:             ENV["S3_BUCKET"],
    distribution_id:       ENV["CLOUDFRONT_DISTRUBTION_ID"],
    build_dir:             ENV["BUILD_DIR"],
    output_changset_path:  ENV["OUTPUT_CHANGESET_PATH"],
    auto_approve:          ENV["AUTO_APPROVE"],
    silent: "ignore,no_change",
    ignore_files: [
      'stylesheets/index',
      'android-chrome-192x192.png',
      'android-chrome-256x256.png',
      'apple-touch-icon-precomposed.png',
      'apple-touch-icon.png',
      'site.webmanifest',
      'error.html',
      'favicon-16x16.png',
      'favicon-32x32.png',
      'favicon.ico',
      'robots.txt',
      'safari-pinned-tab.svg'
    ]
  )
end
```

Create a new folder called sync within ```aws / cfn```, then add template.yaml with the command below:

```sh
AWSTemplateFormatVersion: 2010-09-09
Parameters:
  GitHubOrg:
    Description: Name of GitHub organization/user (case sensitive)
    Type: String
  RepositoryName:
    Description: Name of GitHub repository (case sensitive)
    Type: String
    Default: 'aws-bootcamp-cruddur-2023'
  OIDCProviderArn:
    Description: Arn for the GitHub OIDC Provider.
    Default: ""
    Type: String
  OIDCAudience:
    Description: Audience supplied to configure-aws-credentials.
    Default: "sts.amazonaws.com"
    Type: String

Conditions:
  CreateOIDCProvider: !Equals 
    - !Ref OIDCProviderArn
    - ""

Resources:
  Role:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Statement:
          - Effect: Allow
            Action: sts:AssumeRoleWithWebIdentity
            Principal:
              Federated: !If 
                - CreateOIDCProvider
                - !Ref GithubOidc
                - !Ref OIDCProviderArn
            Condition:
              StringEquals:
                token.actions.githubusercontent.com:aud: !Ref OIDCAudience
              StringLike:
                token.actions.githubusercontent.com:sub: !Sub repo:${GitHubOrg}/${RepositoryName}:*

  GithubOidc:
    Type: AWS::IAM::OIDCProvider
    Condition: CreateOIDCProvider
    Properties:
      Url: https://token.actions.githubusercontent.com
      ClientIdList: 
        - sts.amazonaws.com
      ThumbprintList:
        - 6938fd4d98bab03faadb97b34396831e3780aea1

Outputs:
  Role:
    Value: !GetAtt Role.Arn 
```

Create a new file called config.toml within ```aws / cfn / sync```, then add template.yaml with the command below:

```sh
[deploy]
bucket = 'cfn-artifacts-latino'
region = '$AWS_DEFAULT_REGION'
stack_name = 'CrdSyncRole'

[parameters]
GitHubOrg = 'afrolatino'
RepositoryName = 'aws-bootcamp-cruddur-2023'
OIDCProviderArn = ''
```

Create a new file called sync within ```bin / cfn``` with the command below:

```sh
#! /usr/bin/env bash
set -e # stop the execution of the script if it fails

CFN_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/sync/template.yaml"
CONFIG_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/sync/config.toml"
echo $CFN_PATH

cfn-lint $CFN_PATH

BUCKET=$(cfn-toml key deploy.bucket -t $CONFIG_PATH)
REGION=$(cfn-toml key deploy.region -t $CONFIG_PATH)
STACK_NAME=$(cfn-toml key deploy.stack_name -t $CONFIG_PATH)
PARAMETERS=$(cfn-toml params v2 -t $CONFIG_PATH)

aws cloudformation deploy \
  --stack-name $STACK_NAME \
  --s3-bucket $BUCKET \
  --s3-prefix sync \
  --region $REGION \
  --template-file "$CFN_PATH" \
  --no-execute-changeset \
  --tags group=cruddur-sync \
  --parameter-overrides $PARAMETERS \
  --capabilities CAPABILITY_NAMED_IAM
```

Make the file executable by running ```chmod u+x ./bin/cfn/sync```, then run ```./bin/cfn/sync```

Run ```bundle install```, then ```bundle update --bundler``` to resolve dependencies.

This creates **CrdSyncRole** as seen on the screenshot below:

![CrdSyncRole_created](https://github.com/AfroLatino/aws-bootcamp-cruddur-2023/assets/78261965/cecb06ca-90e4-40c5-97ff-11e7a08899f2)

#### Role Permission added

This creates a role called **CrdSyncRole-Role-177E0006O8UW2**.

- Navigate to Permissions
- Add Permissions -> Create inline policy 
- Navigate to Visual editor
- Select S3 service
- Choose Actions of getObject, PutObject, ListBucket, DeleteObject
- Resources: Leave the default setting of Specific
- Navigate to bucket -> Add ARN (s), Then Bucket name of ocubeltd.co.uk -> Click on Add
- Navigate to object -> Add ARN (s), Then Bucket name of ocubeltd.co.uk and Object name of Any-> Click on Add

See JSON format below:
```sh
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::ocubeltd.co.uk",
                "arn:aws:s3:::ocubeltd.co.uk/*"
            ]
        }
    ]
}
```

- Click on **Review policy**, 
- Name the policy **S3AccessForSync**, 
- Click on **Create Policy**
- Update role-to-assume within ```github/ workflows/ sync.yaml.example``` with the Role's ARN


### Reconnect Database and Post Confirmation Lambda <a name="paragraph2"></a>

Run the commands below:

```sh
./bin/backend/build
./bin/backend/push
./bin/backend/register
```

Amend **PROD_CONNECTION_URL** from **cruddur-db-instance** to **cruddur-instance**

- Navigate to cruddur-instance within RDS in AWS Management Console
- Open the Security Group 
- Navigate to Inbound rules 
- Edit inbound rules
- Choose Type of PostgreSQL
- Choose Source of My IP 
- Note down GITPOD as Description 
- Then, save rules

Run ```./bin/rds/update-sg-rule```

Choose ```Security group rule ID for IPv4```

Then type in ```export DB_SG_RULE_ID="$SECURITY_GROUP_RULE_ID"``` on CLI

Copy the Security Group ID from ```CrdDbRDSSG``` Security Group name, then export ```DB_SG_ID="$SECURITY_GROUP_ID"```

Ensure GITPOD is set by running the command below:

```sh
export GITPOD_IP=$(curl ifconfig.me)
```

Run the commands below:

```sh
./bin/db/connect prod
./bin/db/schema-load prod
```

Amend **CONNECTION_URL** to the command below:

```sh
CONNECTION_URL=$PROD_CONNECTION_URL ./bin/db/migrate
```

This adds the **bio text user**

- Update **environment variable** on **cruddur-post-confirmation lambda**
- Create a new **Security Group**
- Navigate to **Security Groups** from AWS Services
- Name the Security Group **CognitoLambdaSG**
- Choose **non-default VPC**
- Do not specify any inbound rules 
- Navigate to Create
- Navigate to **cruddur-post-confirmation lambda**
- Navigate to **Environment variables**
- Update **CONNECTION_URL** environment variable from **cruddur-db-instance** to **cruddur-instance**
- Navigate to VPC 
- Choose non-default VPC 
- Choose only Public Subnets
- Choose the new Security Group created
- Then, save.

- Navigate to the Security Group for the database
- Edit Inbound rules 
- Add rule of Type PostgreSQL
- Source of Custom and choose the newly created Security Group
- Add a description of **COGNITOPOSTCONF**

Update ```aws/lambdas/cruddur-post-confirrmation.py``` and also the lambda called ```cruddur-post-confirmation``` with the command below:

```sh
import json
import psycopg2
import os

def lambda_handler(event, context):
    user = event['request']['userAttributes']
    print('userAttributes')
    print(user)

    user_display_name  = user['name']
    user_email         = user['email']
    user_handle        = user['preferred_username']
    cognito_user_id    = user['sub']
    try:
      print('entered-try')
      sql = f"""
         INSERT INTO public.users (
          display_name, 
          email,
          handle, 
          cognito_user_id
          ) 
        VALUES(
          %(display_name)s,
          %(email)s,
          %(handle)s,
          %(cognito_user_id)s
        )
      """
      print('SQL Statement ----')
      print(sql)
      conn = psycopg2.connect(os.getenv('CONNECTION_URL'))
      cur = conn.cursor()
      params = {
        'display_name': user_display_name,
        'email': user_email,
        'handle': user_handle,
        'cognito_user_id': cognito_user_id
      }
      cur.execute(sql,params)
      conn.commit() 

    except (Exception, psycopg2.DatabaseError) as error:
      print('error:')
      print(error)
    finally:
      if conn is not None:
          cur.close()
          conn.close()
          print('Database connection closed.')
    return event
```


### Use CORS for Service <a name="paragraph3"></a>

Amend ```config.toml``` file within ```aws/cfn/service``` with the command below:

```sh
[deploy]
bucket = 'cfn-artifacts-afrolatino'
region = '$AWS_DEFAULT_REGION'
stack_name = 'CrdSrvBackendFlask'

[parameters]
EnvFrontendUrl = 'https://ocubeltd.co.uk'
EnvBackendUrl = 'https://api.ocubeltd.co.uk'
```

Amended ```bin/cfn/service``` by removing the comments for the parameters.


### CICD Pipeline and Create Activity <a name="paragraph4"></a>

Amend ```docker-compose.yaml``` so that it is using the standard docker file as opposed to prod version as seen below:

```sh
build:
      context:  ./backend-flask
      dockerfile: Dockerfile
```

Amended ```backend-flask/app.py``` to the command below:

```sh
@app.route("/api/activities", methods=['POST','OPTIONS'])
@cross_origin()
@jwt_required()
def data_activities():
  message = request.json['message']
  ttl = request.json['ttl']
  model = CreateActivity.run(message, g.cognito_user_id, ttl)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
```

Amend ```backend-flask/services/create_activity.py``` to include cognito_user_id as follows:

```sh
class CreateActivity:
  def run(message, cognito_user_id, ttl):
    model = {
      'errors': None,
      'data': None
    }
    
 ---

if cognito_user_id == None or len(cognito_user_id) < 1:
      model['errors'] = ['cognito_user_id_blank']
---

else:
      expires_at = (now + ttl_offset)
      uuid = CreateActivity.create_activity(cognito_user_id,message,expires_at)

      object_json = CreateActivity.query_object_activity(uuid)
      model['data'] = object_json
    return model

  def create_activity(cognito_user_id, message, expires_at):
    sql = db.template('activities','create')
    uuid = db.query_commit(sql,{
      'cognito_user_id': cognito_user_id,
      'message': message,
      'expires_at': expires_at
    })
```

Add another cognito user to the seed data via this path: ```backend-flask/db/seed.sql```

Amend ```backend-flask/db/sql/activities/create.sql``` with the command below:

```sh
INSERT INTO public.activities (
  user_uuid,
  message,
  expires_at
)
VALUES (
  (SELECT uuid 
    FROM public.users 
    WHERE users.cognito_user_id = %(cognito_user_id)s
    LIMIT 1
  ),
  %(message)s,
  %(expires_at)s
) RETURNING uuid;
```

Add the command below to ```frontend-react-js/src/components/ActivityForm.js```:

```sh
import {getAccessToken} from '../lib/CheckAuth';
```

Trigger the CodePipeline

Amend ```aws/cfn/cicd/config.toml``` to include my username as shown below:

```sh
GithubRepo = 'afrolatino/aws-bootcamp-cruddur-2023'
```

Amend ```aws/cfn/cicd/template.yaml``` to include additional permissions as seen below:

```sh
- PolicyName: !Sub ${AWS::StackName}S3ArtifactAccess
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Action:
                - s3:*
                Effect: Allow
                Resource:
                  - !Sub arn:aws:s3:::${ArtifactBucketName}
                  - !Sub arn:aws:s3:::${ArtifactBucketName}/*
```

### Refactor JWT to use a decorator <a name="paragraph5"></a>
