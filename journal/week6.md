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
      "Resource": "arn:aws:ssm:us-east-1::$AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/*"
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
            "Resource": "arn:aws:ssm:us-east-1:097592373482:parameter/cruddur/backend-flask/*"
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

aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/CloudWatchFullAccess --role-name CruddurTaskRole
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess --role-name CruddurTaskRole

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

  
