# Week 6 — Deploying Containers

## Required Homework 

## Deploy an ECS Cluster using ECS Service Connect

### Refactor bin directory to be top level

The bin directory was previously in backend-flask. This was refactored to the top (main) level.

### Test RDS Connection

I added the test script below to check the connection from my container.

```python
#!/usr/bin/env python3

import psycopg
import os
import sys

connection_url = os.getenv("CONNECTION_URL")

conn = None
try:
  print('attempting connection')
  conn = psycopg.connect(connection_url)
  print("Connection successful!")
except psycopg.Error as e:
  print("Unable to connect to the database:", e)
finally:
  conn.close()
```

I made it executable by doing chmod u+x ./bin/db/test, then ./bin/db/test.

### Task Flask Script

I added the following endpoint for my flask app:

```python
@app.route('/api/health-check')
def health_check():
  return {'success': True}, 200
```

I created a new bin script at ./backend-flask/bin/health-check.

```python
#!/usr/bin/env python3

import urllib.request

response = urllib.request.urlopen('http://localhost:4567/api/health-check')
if response.getcode() == 200:
  print("Flask server is running")
else:
  print("Flask server is not running")
```
I made it executable by doing chmod u+x ./backend-flask/bin/health-check.

### Create Log Group

I created a new log group called cruddur.

```sh
aws logs create-log-group --log-group-name "cruddur"
```

Set retention to be 1 day as below:

```sh
aws logs put-retention-policy --log-group-name "cruddur" --retention-in-days 1
```

### Create ECS Cluster

I created an ECS Cluster called cruddur.

```sh
aws ecs create-cluster \
--cluster-name cruddur \
--service-connect-defaults namespace=cruddur
```

![cluster](https://user-images.githubusercontent.com/128761840/229622700-560069cd-66b6-4bfa-a1f7-0c341b748ade.png)

### Create Repository

I created a private repository called cruddur-python using the command below:

```sh
aws ecr create-repository \
  --repository-name cruddur-python \
  --image-tag-mutability MUTABLE
```

![Private_Repo created](https://user-images.githubusercontent.com/128761840/229592376-c533ac8d-c560-4f48-9b48-4f1d57d97695.png)

### Login to ECR

```sh
aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com"
```

### For Base-Image Python
```sh
aws ecr create-repository \
  --repository-name cruddur-python \
  --image-tag-mutability MUTABLE
 ```
 
#### Set URL
```sh
export ECR_PYTHON_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/cruddur-python"
echo $ECR_PYTHON_URL
```

#### Pull Image
```sh
docker pull python:3.10-slim-buster
```

#### Tag Image
```sh
docker tag python:3.10-slim-buster $ECR_PYTHON_URL:3.10-slim-buster
```

#### Push Image
```sh
docker push $ECR_PYTHON_URL:3.10-slim-buster
```

![Image tag created](https://user-images.githubusercontent.com/128761840/229591636-4e01d440-79a7-4e0b-b887-89b774bca0bb.png)


### For Flask

I updated the from to within my flask dockerfile to use my own image as seen below:

```sh
FROM <AWS_ACCOUNT_ID>.dkr.ecr.<AWS_DEFAULT_REGION>.amazonaws.com/cruddur-python:3.10-slim-buster
```

#### Create Repo
```sh
aws ecr create-repository \
  --repository-name backend-flask \
  --image-tag-mutability MUTABLE
  ```
  
#### Set URL
```sh
export ECR_BACKEND_FLASK_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/backend-flask"
echo $ECR_BACKEND_FLASK_URL
```

#### Build Image
```sh
docker build -t backend-flask .
```

#### Tag Image
```sh
docker tag backend-flask:latest $ECR_BACKEND_FLASK_URL:latest
```

#### Push Image
```sh
docker push $ECR_BACKEND_FLASK_URL:latest
``` 

Then, I navigated to Amazon ECS to check for the cluster and images created.

If you want to run and test it, use the command below:

```sh
docker build -f Dockerfile.prod -t backend-flask-prod .
```
```sh
#! /usr/bin/bash

docker run --rm \
-p 4567:4567 \
--env AWS_ENDPOINT_URL="http://dynamodb-local:8000" \
--env CONNECTION_URL="postgresql://postgres:password@db:5432/cruddur" \
--env FRONTEND_URL="https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}" \
--env BACKEND_URL="https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}" \
--env OTEL_SERVICE_NAME='backend-flask' \
--env OTEL_EXPORTER_OTLP_ENDPOINT="https://api.honeycomb.io" \
--env OTEL_EXPORTER_OTLP_HEADERS="x-honeycomb-team=${HONEYCOMB_API_KEY}" \
--env AWS_XRAY_URL="*4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}*" \
--env AWS_XRAY_DAEMON_ADDRESS="xray-daemon:2000" \
--env AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}" \
--env AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
--env AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
--env ROLLBAR_ACCESS_TOKEN="${ROLLBAR_ACCESS_TOKEN}" \
--env AWS_COGNITO_AWS_USER_POOL_ID="${AWS_COGNITO_AWS_USER_POOL_ID}" \
--env AWS_COGNITO_AWS_USER_POOL_CLIENT_ID="${AWS_COGNITO_AWS_USER_POOL_CLIENT_ID}" \
-it backend-flask-prod 
```

### Register Task Definitions

You need to create a parameter first before creating a role.

This can be done via the CLI in the main folder using the commands below:

```sh
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/AWS_ACCESS_KEY_ID" --value $AWS_ACCESS_KEY_ID
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/AWS_SECRET_ACCESS_KEY" --value $AWS_SECRET_ACCESS_KEY
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/CONNECTION_URL" --value $PROD_CONNECTION_URL
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/ROLLBAR_ACCESS_TOKEN" --value $ROLLBAR_ACCESS_TOKEN
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/OTEL_EXPORTER_OTLP_HEADERS" --value "x-honeycomb-team=$HONEYCOMB_API_KEY"
```

After setting these, then navigate to **Systems Manager -> Parameter Store** to check that all the values have been set correctly.

![AWSSystemsManagerParameters](https://user-images.githubusercontent.com/128761840/229592056-facb4196-ca2a-4ca8-a3db-70bb88d3117f.png)

Difference between Service and Task is; as soon as a task finishes executing, it kills itself but a service keeps on running.

### Create Task and Execution Policy and Roles for Task Definition

#### Create Service Execution Policy

Created a new file within aws -> policies called service-execution-policy.json using the script below:
```json
{
    "Version":"2012-10-17",
    "Statement":[{
      "Effect": "Allow",
      "Action": [
        "ssm:GetParameters",
        "ssm:GetParameter"
      ],
      "Resource": "arn:aws:ssm:$AWS_DEFAULT_REGION::$AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/*"
    }]
  }
```

#### Create Execution Role

Created the role called CruddurServiceExecutionRole as seen below: 

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "Service": "ecs-tasks.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

![role screenshot](https://user-images.githubusercontent.com/128761840/229591914-eb4a8d6c-0db8-4629-85b2-74ba9fb11d58.png)


#### Create Execution Policy

Created a policy called CruddurServiceExecutionPolicy in AWS Management Console.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "ssm:GetParameters",
                "ssm:GetParameter"
            ],
            "Resource": "arn:aws:ssm:$AWS_DEFAULT_REGION:$AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/*"
        }
    ]
}
```

![CruddurServiceExecutionPolicy](https://user-images.githubusercontent.com/128761840/229593772-6b5dc562-4ce7-45a1-af8d-ef7a2e57a7e2.png)

#### Create Task Role

Created Task Role using the CLI command below:

```sh
aws iam create-role \
    --role-name CruddurTaskRole \
    --assume-role-policy-document "{
  \"Version\":\"2012-10-17\",
  \"Statement\":[{
    \"Action\":[\"sts:AssumeRole\"],
    \"Effect\":\"Allow\",
    \"Principal\":{
      \"Service\":[\"ecs-tasks.amazonaws.com\"]
    }
  }]
}"
```

![CruddurTaskRole](https://user-images.githubusercontent.com/128761840/229598687-9e2d29d8-8140-40a1-bd66-ee55d493c929.png)

#### Create Role Policy

I created a role policy called SSMAccessPolicy with the CLI command below:

```sh
aws iam put-role-policy \
  --policy-name SSMAccessPolicy \
  --role-name CruddurTaskRole \
  --policy-document "{
  \"Version\":\"2012-10-17\",
  \"Statement\":[{
    \"Action\":[
      \"ssmmessages:CreateControlChannel\",
      \"ssmmessages:CreateDataChannel\",
      \"ssmmessages:OpenControlChannel\",
      \"ssmmessages:OpenDataChannel\"
    ],
    \"Effect\":\"Allow\",
    \"Resource\":\"*\"
  }]
}
"
```

![SSMAccessPolicy](https://user-images.githubusercontent.com/128761840/229598009-e38f72a6-1912-490c-b89f-35ca96303d46.png)

#### Attach Role Policy

```sh
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/CloudWatchFullAccess --role-name CruddurTaskRole
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess --role-name CruddurTaskRole
```

#### Create JSON file

Created a new folder called task-definitions in aws directory, then a new file called backend-flask.json with the script below:

```sh
{
    "family": "backend-flask",
    "executionRoleArn": "arn:aws:iam::$AWS_ACCOUNT_ID:role/CruddurServiceExecutionRole",
    "taskRoleArn": "arn:aws:iam::$AWS_ACCOUNT_ID:role/CruddurTaskRole",
    "networkMode": "awsvpc",
    "cpu": "256",
    "memory": "512",
    "requiresCompatibilities": [ 
      "FARGATE" 
    ],
    "containerDefinitions": [
      {
        "name": "xray",
        "image": "public.ecr.aws/xray/aws-xray-daemon" ,
        "essential": true,
        "user": "1337",
        "portMappings": [
          {
            "name": "xray",
            "containerPort": 2000,
            "protocol": "udp"
          }
        ]
      },
      {
        "name": "backend-flask",
        "image": "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/backend-flask",
        "essential": true,
        "healthCheck": {
          "command": [
            "CMD-SHELL",
            "python /backend-flask/bin/health-check"
          ],
          "interval": 30,
          "timeout": 5,
          "retries": 3,
          "startPeriod": 60
        },
        "portMappings": [
          {
            "name": "backend-flask",
            "containerPort": 4567,
            "protocol": "tcp", 
            "appProtocol": "http"
          }
        ],
        "logConfiguration": {
          "logDriver": "awslogs",
          "options": {
              "awslogs-group": "cruddur",
              "awslogs-region": "us-east-1",
              "awslogs-stream-prefix": "backend-flask"
          }
        },
        "environment": [
          {"name": "OTEL_SERVICE_NAME", "value": "backend-flask"},
          {"name": "OTEL_EXPORTER_OTLP_ENDPOINT", "value": "https://api.honeycomb.io"},
          {"name": "AWS_COGNITO_USER_POOL_ID", "value": $AWS_COGNITO_USER_POOL_ID},
          {"name": "AWS_COGNITO_USER_POOL_CLIENT_ID", "value": $AWS_COGNITO_USER_POOL_CLIENT_ID},
          {"name": "FRONTEND_URL", "value": $FRONTEND_URL},
          {"name": "BACKEND_URL", "value": $BACKEND_URL},
          {"name": "AWS_DEFAULT_REGION", "value": $AWS_DEFAULT_REGION}
        ],
        "secrets": [
          {"name": "AWS_ACCESS_KEY_ID"    , "valueFrom": "arn:aws:ssm:$AWS_DEFAULT_REGION:$AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/AWS_ACCESS_KEY_ID"},
          {"name": "AWS_SECRET_ACCESS_KEY", "valueFrom": "arn:aws:ssm:$AWS_DEFAULT_REGION:$AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/AWS_SECRET_ACCESS_KEY"},
          {"name": "CONNECTION_URL"       , "valueFrom": "arn:aws:ssm:$AWS_DEFAULT_REGION:$AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/CONNECTION_URL" },
          {"name": "ROLLBAR_ACCESS_TOKEN" , "valueFrom": "arn:aws:ssm:$AWS_DEFAULT_REGION:$AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/ROLLBAR_ACCESS_TOKEN" },
          {"name": "OTEL_EXPORTER_OTLP_HEADERS" , "valueFrom": "arn:aws:ssm:$AWS_DEFAULT_REGION:$AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/OTEL_EXPORTER_OTLP_HEADERS" }
        ]
      }
    ]
  }
 ``` 

#### Register Task Definition

Created task definition for the backend-flask using the CLI command below:

```sh
aws ecs register-task-definition --cli-input-json file://aws/task-definitions/backend-flask.json
```

![AmazonECSBackend-flask](https://user-images.githubusercontent.com/128761840/229602672-fab59399-c7d8-42c7-b6b5-3dda7f41d255.png)

#### Create Default VPC_ID

We need the default VPC ID using the command below:
```sh
export DEFAULT_VPC_ID=$(aws ec2 describe-vpcs \
--filters "Name=isDefault, Values=true" \
--query "Vpcs[0].VpcId" \
--output text)

echo $DEFAULT_VPC_ID
```

#### Create Security Group

```sh
export CRUD_SERVICE_SG=$(aws ec2 create-security-group \
  --group-name "crud-srv-sg" \
  --description "Security group for Cruddur services on ECS" \
  --vpc-id $DEFAULT_VPC_ID \
  --query "GroupId" --output text)
  
echo $CRUD_SERVICE_SG
```

![securitygroups](https://user-images.githubusercontent.com/128761840/229622216-16c440bc-67a7-4a9c-8258-e4d7aef98bf0.png)

#### Authorise Security Group

```sh
aws ec2 authorize-security-group-ingress \
  --group-id $CRUD_SERVICE_SG \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0
```

### Create Services
```sh
aws ecs create-service --cli-input-json file://aws/json/backend-flask-serv.json
```

#### Connection via Sessions Manager (Fargate)

```sh
curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/linux_64bit/session-manager-plugin.rpm" -o "session-manager-plugin.rpm"
```

Install for Ubuntu

```sh
curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb" -o "session-manager-plugin.deb"

sudo dpkg -i session-manager-plugin.deb
```

Verify its working

```sh
session-manager-plugin
```

Connect to the container

```sh
aws ecs execute-command  \
--region $AWS_DEFAULT_REGION \
--cluster cruddur \
--task dceb2ebdc11c49caadd64e6521c6b0c7 \
--container backend-flask \
--command "/bin/bash" \
--interactive
```

### For Frontend React

#### Create Repo

```sh
aws ecr create-repository \
  --repository-name frontend-react-js \
  --image-tag-mutability MUTABLE
```
  
#### Set URL

```sh
export ECR_FRONTEND_REACT_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/frontend-react-js"
echo $ECR_FRONTEND_REACT_URL
```

#### Build Image

```sh
docker build \
--build-arg REACT_APP_BACKEND_URL="${REACT_APP_BACKEND_URL}"  \
--build-arg REACT_APP_AWS_PROJECT_REGION="${AWS_DEFAULT_REGION}" \
--build-arg REACT_APP_AWS_COGNITO_REGION="${AWS_DEFAULT_REGION}" \
--build-arg REACT_APP_AWS_USER_POOLS_ID="${AWS_COGNITO_AWS_USER_POOL_ID}"  \
--build-arg REACT_APP_CLIENT_ID="${AWS_COGNITO_AWS_USER_POOL_CLIENT_ID}"  \
-t frontend-react-js \
-f Dockerfile.prod \
.
```

#### Tag Image

```sh
docker tag frontend-react-js:latest $ECR_FRONTEND_REACT_URL:latest
```

#### Push Image

```sh
docker push $ECR_FRONTEND_REACT_URL:latest
```

If you want to run and test it, use the command below:

```sh
docker run --rm -p 3000:3000 -it frontend-react-js 
```

### Create Task and Services and Roles for Task Definition - Frontend React

#### Create JSON file

Created a new folder called task-definitions in aws directory, then a new file called frontend-react-js.json with the script below:

```sh
{
    "family": "frontend-react-js",
    "executionRoleArn": "arn:aws:iam::$AWS_ACCOUNT_ID:role/CruddurServiceExecutionRole",
    "taskRoleArn": "arn:aws:iam::$AWS_ACCOUNT_ID:role/CruddurTaskRole",
    "networkMode": "awsvpc",
    "cpu": "256",
    "memory": "512",
    "requiresCompatibilities": [ 
      "FARGATE" 
    ],
    "containerDefinitions": [
      {
        "name": "xray",
        "image": "public.ecr.aws/xray/aws-xray-daemon" ,
        "essential": true,
        "user": "1337",
        "portMappings": [
          {
            "name": "xray",
            "containerPort": 2000,
            "protocol": "udp"
          }
        ]
      },
      {
        "name": "frontend-react-js",
        "image": "$AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/frontend-react-js",
        "essential": true,
        "healthCheck": {
          "command": [
            "CMD-SHELL",
            "curl -f http://localhost:3000 || exit 1"
          ],
          "interval": 30,
          "timeout": 5,
          "retries": 3
        },
        "portMappings": [
          {
            "name": "frontend-react-js",
            "containerPort": 3000,
            "protocol": "tcp", 
            "appProtocol": "http"
          }
        ],
  
        "logConfiguration": {
          "logDriver": "awslogs",
          "options": {
              "awslogs-group": "cruddur",
              "awslogs-region": "us-east-1",
              "awslogs-stream-prefix": "frontend-react-js"
          }
        }
      }
    ]
  }
```

#### Register Task Defintion

```sh
aws ecs register-task-definition --cli-input-json file://aws/task-defintions/frontend-react-js.json
```

![task definitions](https://user-images.githubusercontent.com/128761840/229613471-81d2c5e4-02e9-423e-8c30-c16846d539a2.png)


#### Create Services

```sh
aws ecs create-service --cli-input-json file://aws/json/frontend-react-js-serv.json
```

![servicescreated](https://user-images.githubusercontent.com/128761840/229612984-ee78b9b5-14c7-4441-90fb-948f8ee6ec0c.png)

### Run Before Docker Compose

```sh
./bin/ecr/login
./bin/backend/generate-env
./bin/frontend/generate-env
```

Steps needed

```sh
./bin/backend/build
./bin/backend/push
./bin/backend/register
./bin/backend/deploy
```

### Load Balancer

Elastic Load Balancing automatically distributes your incoming traffic across multiple targets, such as EC2 instances, containers, and IP addresses, in one or more Availability Zones. It monitors the health of its registered targets, and routes traffic only to the healthy targets. Elastic Load Balancing scales your load balancer as your incoming traffic changes over time. It can automatically scale to the vast majority of workloads.

A load called cruddur-alb was created in AWS EC2.

![LoadBalancer](https://user-images.githubusercontent.com/128761840/229615569-1014c53a-b49f-4cbc-b7b9-4af88d1b90b6.png)

#### Application Load Balancer components

A load balancer serves as the single point of contact for clients. The load balancer distributes incoming application traffic across multiple targets, such as EC2 instances, in multiple Availability Zones. This increases the availability of your application. You add one or more listeners to your load balancer.

A listener checks for connection requests from clients, using the protocol and port that you configure. The rules that you define for a listener determine how the load balancer routes requests to its registered targets. Each rule consists of a priority, one or more actions, and one or more conditions. When the conditions for a rule are met, then its actions are performed. You must define a default rule for each listener, and you can optionally define additional rules.

Each target group routes requests to one or more registered targets, such as EC2 instances, using the protocol and port number that you specify. You can register a target with multiple target groups. You can configure health checks on a per target group basis. Health checks are performed on all targets registered to a target group that is specified in a listener rule for your load balancer.

The following diagram illustrates the basic components. Notice that each listener contains a default rule, and one listener contains another rule that routes requests to a different target group. One target is registered with two target groups.

![LoadBalancerPic](https://user-images.githubusercontent.com/128761840/229616459-df3b1e53-d0bf-4299-8ee8-b1985b76998a.png)

**Target Groups**

2 Target Groups called cruddur-backend-flask-tg and cruddur-frontend-react-js were created as seen below:

![TargetGroups](https://user-images.githubusercontent.com/128761840/229620560-3ec93798-3e9f-45b4-8e52-02de7757821a.png)

**Listeners**

2 listeners called HTTPS:443 and HTTP:80 were created.

![listenersadded](https://user-images.githubusercontent.com/128761840/229617429-6ca10596-c239-4a15-a53f-4a3e1bf2ba2a.png)

The rules below were added to these listeners:

- HTTPS:443: IF Host is FRONTEND_URL, THEN forward to cruddur-backend-flask-tg: 1 (100%) and for HTTPS 443: default action, IF Requests otherwise not routed THEN
Forward to cruddur-frontend-react-js.
- HTTP:80: For HTTP 80: default action, IF Requests otherwise not routed THEN Redirect to https://#{host}:443/#{path}?#{query} Status code:HTTP_302 

![rulescreated](https://user-images.githubusercontent.com/128761840/229618908-2865f526-68f0-48a1-b739-22125fbce12b.png)

![HTTP80 rule](https://user-images.githubusercontent.com/128761840/229619453-11fd6ac9-abbf-4c7d-b37c-becac908ad8c.png)

**Inbound rules set for VPCs**

Inbound rules were set for the load balancer and the crud security group

![Inboundrulesforsrvsg](https://user-images.githubusercontent.com/128761840/229623547-e777cbe6-c889-415f-8a91-98d73cdcb865.png)

![Inboundrulesforalbsg](https://user-images.githubusercontent.com/128761840/229623561-d9a13156-af52-4a76-9caa-3fc4a734f81f.png)

**Reference**

[Elastic Load Balancing](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html)


### Managing my domain using Route53 via hosted zone

A domain name is required to complete this project in order for the backend to talk to the frontend via the web browser.

I managed my domain using Route53 via hosted zone as seen below:

![hostedzone](https://user-images.githubusercontent.com/128761840/229624328-f4b21c31-6d78-4745-ac5f-70df86312c33.png)

### Create an SSL cerificate via ACM

I created an SSL certificate via ACM as seen below:

![AWSCertManager](https://user-images.githubusercontent.com/128761840/229624889-408e6626-c266-431d-979e-c9981ef6c732.png)


## Amazon ECS Security Best Practices

### Table of contents
- [Container Security Status in 2022](#introduction)
- [Container Services in AWS](#paragraph1)
- [Types of Launch Type to AWS](#paragraph2)
- [Shared Risk with AWS ECS](#paragraph3)
    - [Sharing Responsibilities in a managed service model](#subparagraph1)
- [Security Challenges with AWS Fargate](#paragraph4)
- [Amazon ECS (EC2) Setup](#paragraph5)
     - [Creating a Repository](#subparagraph2)
     - [Amazon Elastic Container Service](#subparagraph3)
     - [Amazon ECR Images Security](#subparagraph4)
- [Amazon ECS – Security Best Practices – AWS](#paragraph6)
- [Amazon ECS – Security Best Practices – Application](#paragraph7)


### Container Security Status in 2022 <a name="introduction"></a>

- 75% of containers run with "high" or "critical" vulnerabilities
- 50% of containers have no limits defined
- 76% of containers run as root

### Container Services in AWS <a name="paragraph1"></a>

-	Virtual Machine
-	ECS, Fargate, EKS

### Types of Launch Type to AWS <a name="paragraph2"></a>

- Amazon EC2 architecture: This includes Elastic Load Balancing (ELB), Auto Scaling groups and Amazon EC2 instances.
-	Amazon ECS architecture: This includes Elastic Load Balancing (ELB), Amazon ECS cluster, Auto Scaling groups and Amazon EC2 instances.
-	ECS Fargate: This includes Elastic Load Balancing (ELB), Amazon ECS cluster and Fargate tasks.

### Shared Risk with AWS ECS <a name="paragraph3"></a>

#### Sharing Responsibilities in a managed service model <a name="subparagraph1"></a>

**Traditional ECS instances**

| **User Manages**     | **AWS Manages** | 
| :---        |    :----:   |          
|Containerized Applications      | Virtual Machine       | 
|Container Runtime  | Physical Server        | 
|Storage, Logging, Monitoring Plugins      |        | 
|Operating System |         | 

**AWS Fargate**

| **User Manages**     | **AWS Manages** | 
| :---        |    :----:   |          
|Containerized Applications      | Container Runtime      | 
|  | Storage, Logging, Monitoring Plugins        | 
|      |Operating System        | 
| | Virtual Machine        | 
| |Physical Server        |

### Security Challenges with AWS Fargate <a name="paragraph4"></a>
- No visibility of Infrastructure
- Ephemeral Resources makes it hard to do triage or Forensics for detected threats
- No file/network monitoring
- Cannot run traditional Security Agents in Fargate
- User can run unverified Container images
- Containers can run as root and even with elevated privileges

### Amazon ECS (EC2) Setup  <a name="paragraph5"></a>
If building a machine with containers, images are needed.

Then navigate to Elastic Container Registry (ECR) on AWS.

#### Creating a Repository <a name="subparagraph2"></a>
- In creating a repository owned by a company, security best practice would be to choose private visibility settings
- Enable tag immutability
- Enable Scan on push
- Enable KMS encryption

After creating ECR, the application will be created in Amazon Elastic Container Service.

#### Amazon Elastic Container Service <a name="subparagraph3"></a>
- Create cluster
- Create Amazon EC2 instances 
       - You'd choose a minimum of 1 and maximum of 2 desired capacity. 
       - Choose Amazon Linux 2 for Operating system/Architecture.
       -  Choose t2.micro as EC2 instance type.
       - SSH Key Pair should be none 
- Add tags – It is always a good practice to add tags.
- Create new task definition on ECS

#### Amazon ECR Images Security <a name="subparagraph4"></a>
- This is linked to Amazon Inspector
- It is using Synk in the background to find vulnerabilities

### Amazon ECS – Security Best Practices – AWS <a name="paragraph6"></a>
- Cloud Control Plane Configuration – Access Control, Container Images etc
- Choosing the right Public or Private ECR for Images
- Amazon ECR Scan Images to "Scan on Push" using Basic or Enhanced (Inspector + Synk)
- Use VPC Endpoints or Security Groups with known sources only.
- Compliance standard is what your business requires.
- Amazon Organisations SCP – To manage ECS Task deletion, ECS creation, region lock etc.
- AWS CloudTrail is enabled & monitored to trigger alerts on malicious ECS behaviour by an identity in AWS.

### Amazon ECS – Security Best Practices – Application <a name="paragraph7"></a>

- Access Control – Roles or IAM Users for ECS Clusters/Services/Tasks
- Most recent version of ECR Agent daemon on EC2
- Container Control Plane Configuration – Root privileges, resource limitations etc.
- No secrets/passwords in ECS Task Definitions e.g. db password etc – Consider AWS Secret Manager.
- No secrets/passwords in Containers – Consider AWS Secret Manager.
- Only use Trusted Containers from ECR with no HIGH/CRITICAL vulnerabilities.
- Limit ability to ssh into EC2 container to read only file systems – Use APIs or GitOps to pull information for troubleshooting.
- Amazon CloudWatch to monitor malicious ECS configuration changes.
- Only using Authorized Container images (hopefully some image signing in the future e.g. sigstore).
- AWS Config Rules (as no GuardDuty (ECS) even in Mar 2023) is enabled in the account and region of ECS.

## My Journey to the Cloud assessment

I AM GOING TO BECOME A: ........Data Engineer.........

I AM A GOOD FIT BECAUSE: .....I have many years of experience with SQL development and analysis.........

| **I WILL KNOW:**     | **I WILL NOT GET DISTRACTED BY:** | 
| :---        |    ----   |          
|1. Python      |1. React JS      | 
|2. Databases (SL, NoSQL etc)  |2. Django        | 
|3. AWS      |3. Kubernetes       | 
|4. Docker | 4. Java        | 
|5. Snowflake        |5. C++  |


## What Cloud Hiring Managers Want from Your Resume

### Write Fears + Dreams of Hiring Manager

| **Fears**     | **Dreams** | 
| :---        |    ----   |          
|1. Last hire had candidates with certifications but were slow to onboard on the job      |1. Demonstration of proficiency in the tech stack used      | 
|2. Candidate need lots of teaching  |2. Fulfilment of the needs of the organisation        | 
|3. Candidate have certifications but no practical knowledge      |3. The candidate knows and care about costs      | 
|4. The candidate has only worked in a particular sector, so may not fit in e.g. a public sector worker coming from a relaxed environment looking for work in the private sector that is fast-paced | 4. The candidate has a service-oriented mindset        | 
|5. The candidate may take a position with another company after a short time with their company.        |5. The candidate knows what is going on in the cloud computing industry  |
|6. Fear of Lawsuits or being called out for iiases | 6. The candidate automates processes and reduce manual or repetitive tasks where possible.  |

  
