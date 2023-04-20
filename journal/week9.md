# Week 9 — CI/CD with CodePipeline, CodeBuild and CodeDeploy

## Required Homework 

### Creating a Pipeline

- Step 1: Create new pipeline
- Step 2: Choose pipeline settings
- Step 3: Name pipeline. I called this **cruddur-backend-fargate**
- Step 4: Leave the default settings of New service role and Allow AWS CodePipeline to create a service role so that it can be used with this new pipeline
- Step 5: In advanced settings, leave the Default location and Default AWS Managed Key
- Step 6: Add Source Stage: Choose **GitHub (Version 2)**
- Step 7: Create a GitHub Connection by clicking on Connect to GitHub
- Step 8: Select **Connection name** as **cruddur**, then connect to GitHub
- Step 9: Install a new app
- Step 10: Enter your GitHub password
- Step 11: Select the Repo needed. In this case, this would be the aws-bootcamp-cruddur-2023 repository.
- Step 12: Then save. If the connection is successful, this would show a number on the GitHub Apps search
- Step 13: Then click on Connect
- Step 14: Select the repo name from the drop-down options
- Step 15: Create a new branch from Main called **prod** on GitHub and choose this as the branch name
- Step 16: Change detection options. Leave the default settings of **Start the pipeline on source code changes** & **CopePipeline Default**
- Step 17: Then Next
- Step 18: Skip build stage for now
- Step 19: Add Deploy Stage - Choose Amazon ECS
- Step 20: For Deploy - Amazon ECS is the Deploy provider, Choose your Region, Select **cruddur** as the **Cluster Name** and **backend-flask** as the **Service name**
- Step 21: Create Pipeline
- Step 22: Primary source webhook events - Choose Rebuild every time a code change is pushed to this repository
- Step 23: Select Single build
- Step 24: Select PULL_REQUEST_MERGED event type
- Step 25: Environment - Leave defualt setting of **Managed image**
- Step 26: Select **Amazon Linux 2** as the **Operating system**
- Step 27: Select **Standard** as **Runtime**
- Step 28: Select the latest version for **Image**. As of 20th April, 2023, this is **aws/codebuild/amazonlinux2-x86_64-standard:4.0**
- Step 29: Select **Linux 2** as the Environment type
- Step 30: For **Privilege**, ensure you tick the checkbox for **Enable this flag if you want to build Docker images or want your builds to get elevated privileges**.   If this box is not checked, you will be unable to build any docker image.
- Step 31: Leave the default settings for **New service role**
- Step 32: Under additional configuration, enter **20mins** for **Timeout**7
- Step 33: Leave the Queued timeout as 8 hours
- Step 34: Leave the default settings of **Do npt install any certificate**
- Step 35: Do not choose any VPC
- Step 36: Leave the default settings for **Compute** as **3 GB memory, 2 vCPUs**

### Buildspec

Create buildspec.yml file

Add the buildspec.yml file below to the backend-flask directory

```yaml
# Buildspec runs in the build stage of your pipeline.
version: 0.2
phases:
  install:
    runtime-versions:
      docker: 20
    commands:
      - echo "cd into $CODEBUILD_SRC_DIR/backend"
      - cd $CODEBUILD_SRC_DIR/backend-flask
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $IMAGE_URL
  build:
    commands:
      - echo Build started on `date`
      - echo Building the Docker image...          
      - docker build -t backend-flask .
      - "docker tag $REPO_NAME $IMAGE_URL/$REPO_NAME"
  post_build:
    commands:
      - echo Build completed on `date`
      - echo Pushing the Docker image..
      - docker push $IMAGE_URL/$REPO_NAME
      - cd $CODEBUILD_SRC_DIR
      - echo "imagedefinitions.json > [{\"name\":\"$CONTAINER_NAME\",\"imageUri\":\"$IMAGE_URL/$REPO_NAME\"}]" > imagedefinitions.json
      - printf "[{\"name\":\"$CONTAINER_NAME\",\"imageUri\":\"$IMAGE_URL/$REPO_NAME\"}]" > imagedefinitions.json

env:
  variables:
    AWS_ACCOUNT_ID: $ACCOUNT_ID
    AWS_DEFAULT_REGION: $AWS_DEFAULT_REGION
    CONTAINER_NAME: backend-flask
    IMAGE_URL: $ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
    REPO_NAME: backend-flask:latest
artifacts:
  files:
    - imagedefinitions.json
```

- For Build specifications, choose **Use a buildspec file**
- Buildspec name is **backend-flask/buildspec.yml**
- Choose the Default settings of **No artificants** Type
- For Additional Configuration, Leave the default settings of **CloudWatch logs**
- Enter **/cruddur/build/backend-flask** as the **Group name**
- Enter **backend-flask** as the **Stream name**
- Then **Create build project**

![create_pipeline](https://user-images.githubusercontent.com/129978840/233218233-039c89a2-cbb5-4a21-9dde-7955fb1f2e20.png)

### CodeBuild

The build project is called **cruddur-backend-flask-bake-image**

Copy the **Copy badge URL** onto a URL. This was added to my GitHiub main repo as seen below:

![Codebuildimage](https://user-images.githubusercontent.com/129978840/233244126-fa36a435-eff7-4567-9106-f7da828f4a3f.png)

Create a pull request from GitHub and merge main into prod

Please see below of the codebuild project.

![codebuild built](https://user-images.githubusercontent.com/129978840/233245850-8f0be418-6f34-428a-9f14-15a60fccc4b8.png)

### IAM Service Role Permissions

I added the JSON permissions below to the IAM service role created called **codebuild-cruddur-backend-flask-bake-image-service-role** 

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ecr:BatchCheckLayerAvailability",
                "ecr:BatchGetImage",
                "ecr:CompleteLayerUpload",
                "ecr:GetAuthorizationToken",
                "ecr:DescribeImages",
                "ecr:DescribeRepositories",
                "ecr:GetDownloadUrlForLayer",
                "ecr:GetLifecyclePolicy",
                "ecr:GetLifecyclePolicyPreview",
                "ecr:GetRepositoryPolicy",
                "ecr:InitiateLayerUpload",
                "ecr:ListImages",
                "ecr:PutImage",
                "ecr:PutLifecyclePolicy",
                "ecr:SetRepositoryPolicy",
                "ecr:StartLifecyclePolicyPreview",
                "ecr:UploadLayerPart"
            ],
            "Resource": "*"
        }
    ]
}
```

Please see the screenshot below for the IAM permissions:

![codebuildIAMrole](https://user-images.githubusercontent.com/129978840/233247785-8d656795-4780-45e6-9201-24756ec26d26.png)

## Amazon CI/CD Pipeline Security on AWS

### Table of contents
- [Introduction](#introduction)
- [Open Worldwide Application Security Project (OWASP) Top 10 C/CD Security Risks](#paragraph1)
- [Amazon CI/CD Pipeline – Security Best Practices – AWS](#paragraph2)
- [Amazon CI/CD Pipeline – Security Best Practices – Application](#paragraph3)

### Introduction <a name="introduction"></a>

CI/CD stands for Continuous Integration/Continuous Deployment or Delivery depending on who you talk to.

Source Code Repository is all the code required to build an application at any given point in time.

AWS Services that can help to deploy a CI/CD pipeline are as follows:
- CodeCommit
- CodeBuild 
- CodeDeploy
- CodePipeline

### Open Worldwide Application Security Project (OWASP) Top 10 C/CD Security Risks <a name="paragraph1"></a>

Open Worldwide Application Security Project (OWASP) Top 10 C/CD Security Risks are as follows: 

- Insufficient Flow Control Mechanisms
- Inadequate Identity and Access Management
- Dependency Chain Abuse
- Poisoned Pipeline Execution (PPE)
- Insufficient PBAC (Pipeline-Based Access Controls)
- Insufficient Credential Hygiene
- Insecure System Configuration
- Ungoverned Usage of 3rd Party Services
- Improper Artifact Integrity Validation
- Insufficient Logging and Visibility

### Amazon CI/CD Pipeline – Security Best Practices – AWS <a name="paragraph2"></a>

-	Compliance standard is what your business requires from a CI/CD service and it is available in the region you need to operate in.
-	Amazon Organisations SCP – to restrict actions like creation, deletion, modification of production CI/CD pipeline services etc.
-	AWS CloudTrail is enabled & monitored to trigger alerts for malicious activities e.g. changes to Production CodePipeline etc.
-	GuardDuty is enabled for monitoring suspicious DNS comms (e.g. Crypto-mining etc) and automated for auto-remediation.
-	AWS Config Rules is enabled in the account and region of CodeBuild – conformance pack for any other CI/CD service.

### Amazon CI/CD Pipeline – Security Best Practices – Application <a name="paragraph3"></a>

-	Access Control – Roles or IAM Users for making changes in Amazon CICD services especially production related repositories, pipeline, build services etc.
-	Security of the CI/CD Pipeline – Source control, Secret Management, Container Registry, CI/CD Service (if not the AWS Service), IAM etc.
-	Security in the CI/CD Pipeline – Code Security Best Practices – SCA, SAST, Secret Scanner, DAST implemented in the CI/CD Pipeline.
-	Security of the CI/CD Pipeline entry points e.g. no bypass of CI/CD to make production changes.
-	Enable Encryption in Transit using TLS/SSL certification e.g. HTTPS
-	Only use Trusted Source Control for sending changes to CI/CD Pipeline
-	Develop process for continuously verifying if there is a change that may compromise the known state of a CI/CD Pipeline.  





