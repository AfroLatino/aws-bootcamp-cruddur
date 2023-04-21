# Week 9 — CI/CD with CodePipeline, CodeBuild and CodeDeploy

## Required Homework 

## Table of contents
- [Introduction](#introduction)
- [CodePipeline for Backend Flask](#paragraph1)
- [Create Build Project](#paragraph2)
- [IAM Service Role Permissions](#paragraph3)
- [Creating the Build Stage of CodePipeline](#paragraph4)
- [Amendment of app.py file](#paragraph5)
- [CodeBuild](#paragraph6)
- [CodeDeploy](#paragraph7)

## Homework Challenges

## Table of contents

- [CodePipeline for Frontend React JS](#paragraph8)


### Introduction <a name="introduction"></a>

An integral part of development operations (DevOps) is adopting the culture of continuous integration and continuous delivery/deployment (CI/CD). Level up with tools to compile, build, and install features and fixes with collaborative and automated processes. These processes allow you to control versioning of your applications through a low-risk mechanism that enables agile, secure deployment and updates. CI/CD helps you keep up the pace of innovation while maintaining maximum uptime for your users.

**AWS CodePipeline** is a fully managed continuous delivery service that helps you automate your release pipelines for fast and reliable application and infrastructure updates.

![codepipeline](https://user-images.githubusercontent.com/129978840/233638485-2b769f6d-d90d-4113-a7c2-b4a7bfecef90.png)

**AWS CodeBuild** is a fully managed build service in the cloud. CodeBuild compiles your source code, runs unit tests, and produces artifacts that are ready to deploy. CodeBuild eliminates the need to provision, manage, and scale your own build servers. 
Reference

**AWS CodeDeploy** is a deployment service that automates application deployments to Amazon EC2 instances, on-premises instances, serverless Lambda functions, or Amazon ECS services.

**References**

[Amazon Docs - CI-CD](https://aws.amazon.com/solutions/app-development/ci-cd/)

[Amazon Docs - CodePipeline](https://aws.amazon.com/codepipeline/)

[Amazon Docs - CodeBuild](https://docs.aws.amazon.com/codebuild/latest/userguide/welcome.html)

[Amazon Docs - CodeDeploy](https://docs.aws.amazon.com/codedeploy/latest/userguide/welcome.html)


### CodePipeline for Backend Flask <a name="paragraph1"></a>

Below are the steps needed for creating a CodePipeline:

- Search for CodePipeline amongst AWS Services. Then, navigate to the screen and click on **Create pipeline**.
- **Step 1: Choose Pipeline Settings**
  - This opens up pipeline settings -> Choose pipeline settings
  - Name pipeline. I called this **cruddur-backend-fargate**
  - Leave the default setting of **New service role**. This automatically creates the **Role name**
  - Leave the default setting of **Allow AWS CodePipeline to create a service role so that it can be used with this new pipeline**
  - Under **Advanced settings**, select **Default location** and leave the default setting of **Default AWS Managed Key**
  - Click on **Next**  
- **Step 2: Add source stage**
   - Select **GitHub (Version 2)** as the **Source provider**
   - Create a GitHub Connection by clicking on **Connect to GitHub**
   - Type **cruddur* as **Connection name**, then **Connect to GitHub**
   - Click on **Install a new app**
   - Enter your GitHub password
   - Select the Repository needed. In this case, this would be the **aws-bootcamp-cruddur-2023 repository**.
   - Then, save. If the connection is successful, this would show a number on the GitHub Apps search
   - Then, click on **Connect**
   - Select the repo name from the drop-down options
   - Create a new branch from Main called **prod** on GitHub and choose this as the branch name
   - Change detection options. Leave the default settings of **Start the pipeline on source code change** & **CopePipeline Default**
   - Select **CodePipeline default** as the **Output artifact format**
   - Click on **Next**
   - Click on **Skip build stage** for now as this is *optional*
   - Click on **Skip**
- **Step 4: Add deploy stage**
   - Select **Amazon ECS** as the **Deploy provider**
   - Region should be automatically loaded but if not, select your **Region**
   - Select **cruddur** as the **Cluster Name** and **backend-flask** as the **Service name**
   - Click on **Next**
   - Then **Create pipeline**
   - Click on **Next**

In order to create the build stage, navigate to **Build projects** on the **Developer Tools**
   - Click on **Create build project**. The **Project name** is **cruddur-backend-flask-bake-image**
   - Click on the tickbox for **Enable build badge**
   - For Source, **Source provider** is **GitHub**
   - Select **Connect using OAuth**
   - Connect to GitHub, then authorize
   - Create Pipeline
   - **Primary source webhook events**. Click on the tickbox for **Choose Rebuild every time a code change is pushed to this repository**
   - Select **Build type** of **Single build**
   - Select **Event type** of **PULL_REQUEST_MERGED**
   - Under **Environment**, leave default setting of **Managed image**
   - Select **Amazon Linux 2** as the **Operating system**
   - Select **Runtime** as **Standard** 
   - Select the **Image** of **aws/codebuild/amazonlinux2-x86_64-standard:4.0**. This is the latest version for Image as of 20th April, 2023.
   - The **Image Version** of **Always use the latest image for this runtime version** will be automatically selected.
   - Select **Environment type** of **Linux 2**
   - For **Privilege**, ensure you tick the checkbox for **Enable this flag if you want to build Docker images or want your builds to get elevated privileges**. If 
     this box is not checked, you will be unable to build any docker image.
   - Leave the default setting of **New service role**
   - Under **Additional configuration**, enter **20mins** for **Timeout**
   - Leave the default setting for **Queued timeout** as 8 hours
   - Leave the default setting of **Do not install any certificate**
   - Do not choose any VPC
   - Leave the default setting for **Compute** as **3 GB memory, 2 vCPUs**
   

### Create Build Project <a name="paragraph2"></a>

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

- Under **Buildspec**, for Build specifications, choose **Use a buildspec file**
- **Buildspec name** is **backend-flask/buildspec.yml**
- Choose the Default setting of **No artifacts** Type
- Under **Logs**, leave the default setting of **CloudWatch logs**
- Enter **/cruddur/build/backend-flask** as the **Group name**
- Enter **backend-flask** as the **Stream name**
- Then click on **Create build project**

Please find below the screen shot for the created CodePipeline.

![create_pipeline](https://user-images.githubusercontent.com/129978840/233218233-039c89a2-cbb5-4a21-9dde-7955fb1f2e20.png)


### IAM Service Role Permissions <a name="paragraph3"></a>

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


### Creating the Build Stage of CodePipeline <a name="paragraph4"></a>

The build stage was earlier skipped during the code pipeline creation.

- Choose existing code pipeline of **cruddur-backend-fargate**
- Click on **Edit**
- Click on **Add Stage** after **Edit: Source**
- Name the **Stage name** as **build**
- Click on **Add stage**
- Cloick on **Add action group** and add **Action name** of **bake**
- Select **Action provider** of **AWS CodeBuild**
- Choose **SourceArtifact** as **Input artifacts**
- Select **cruddur-backend-flask-bake-image** as the **Project name** which was earlier created. 
- Leave the default setting of **Single build** as the **Build type**
- Added **ImageDefinition** as **Output artifacts**
- Then, click on **Done**
- Run this by clicking on **Release change**


### Amendment of app.py file <a name="paragraph5"></a>

I amended app.py with the code below:

```sh
@app.route('/api/health-check')
def health_check():
  return {'success': True, 'ver': 1}, 200
```  
- Created a pull request from **prod** to **Main**


### CodeBuild <a name="paragraph6"></a>

The build project is called **cruddur-backend-flask-bake-image**

Copy the **Copy badge URL** onto a URL. This was added to my GitHiub main repo as seen below:

![Codebuildimage](https://user-images.githubusercontent.com/129978840/233244126-fa36a435-eff7-4567-9106-f7da828f4a3f.png)

Create a pull request from GitHub and merge main into prod

Please see below a screen shot of the Codebuild project.

![codebuild built](https://user-images.githubusercontent.com/129978840/233245850-8f0be418-6f34-428a-9f14-15a60fccc4b8.png)


### CodeDeploy  <a name="paragraph7"></a>

Go to CodeBuild and **Start build with overrides**

Please find below screenshots of the code, build and deploy screens of **Successful**

![sourceandbuildcompleted](https://user-images.githubusercontent.com/129978840/233253714-89363ea0-a353-4e93-be8f-2a6bfe5f35b0.png)

![deploysucceeded](https://user-images.githubusercontent.com/129978840/233253729-ffadf26b-abfc-4240-b5e0-fdd16cfe376f.png)


## Stretch Challenges

### CodePipeline for Frontend React JS <a name="paragraph7"></a>

Below are the steps needed for creating a CodePipeline:

- Search for CodePipeline amongst AWS Services. Then, navigate to the screen and click on **Create pipeline**.
- **Step 1: Choose Pipeline Settings**
  - This opens up pipeline settings -> Choose pipeline settings
  - Name pipeline. I called this **cruddur-backend-fargate**
  - Leave the default setting of **New service role**. This automatically creates the **Role name**
  - Leave the default setting of **Allow AWS CodePipeline to create a service role so that it can be used with this new pipeline**
  - Under **Advanced settings**, select **Default location** and leave the default setting of **Default AWS Managed Key**
  - Click on **Next**  
- **Step 2: Add source stage**
   - Select **GitHub (Version 2)** as the **Source provider**
   - Create a GitHub Connection by clicking on **Connect to GitHub**
   - Type **cruddur* as **Connection name**, then **Connect to GitHub**
   - Click on **Install a new app**
   - Enter your GitHub password
   - Select the Repository needed. In this case, this would be the **aws-bootcamp-cruddur-2023 repository**.
   - Then, save. If the connection is successful, this would show a number on the GitHub Apps search
   - Then, click on **Connect**
   - Select the repo name from the drop-down options
   - Create a new branch from Main called **prod** on GitHub and choose this as the branch name
   - Change detection options. Leave the default settings of **Start the pipeline on source code change** & **CopePipeline Default**
   - Select **CodePipeline default** as the **Output artifact format**
   - Click on **Next**
   - Click on **Skip build stage** for now as this is *optional*
   - Click on **Skip**
- **Step 4: Add deploy stage**
   - Select **Amazon ECS** as the **Deploy provider**
   - Region should be automatically loaded but if not, select your **Region**
   - Select **cruddur** as the **Cluster Name** and **backend-flask** as the **Service name**
   - Click on **Next**
   - Then **Create pipeline**
   - Click on **Next**

In order to create the build stage, navigate to **Build projects** on the **Developer Tools**
   - Click on **Create build project**. The **Project name** is **cruddur-backend-flask-bake-image**
   - Click on the tickbox for **Enable build badge**
   - For Source, **Source provider** is **GitHub**
   - Select **Connect using OAuth**
   - Connect to GitHub, then authorize
   - Create Pipeline
   - **Primary source webhook events**. Click on the tickbox for **Choose Rebuild every time a code change is pushed to this repository**
   - Select **Build type** of **Single build**
   - Select **Event type** of **PULL_REQUEST_MERGED**
   - Under **Environment**, leave default setting of **Managed image**
   - Select **Amazon Linux 2** as the **Operating system**
   - Select **Runtime** as **Standard** 
   - Select the **Image** of **aws/codebuild/amazonlinux2-x86_64-standard:4.0**. This is the latest version for Image as of 20th April, 2023.
   - The **Image Version** of **Always use the latest image for this runtime version** will be automatically selected.
   - Select **Environment type** of **Linux 2**
   - For **Privilege**, ensure you tick the checkbox for **Enable this flag if you want to build Docker images or want your builds to get elevated privileges**. If 
     this box is not checked, you will be unable to build any docker image.
   - Leave the default setting of **New service role**
   - Under **Additional configuration**, enter **20mins** for **Timeout**
   - Leave the default setting for **Queued timeout** as 8 hours
   - Leave the default setting of **Do not install any certificate**
   - Do not choose any VPC
   - Leave the default setting for **Compute** as **3 GB memory, 2 vCPUs**
   

## Amazon CI/CD Pipeline Security on AWS

### Table of contents
- [Introduction](#introduction1)
- [Open Worldwide Application Security Project (OWASP) Top 10 C/CD Security Risks](#paragraph11)
- [Amazon CI/CD Pipeline – Security Best Practices – AWS](#paragraph12)
- [Amazon CI/CD Pipeline – Security Best Practices – Application](#paragraph13)

### Introduction <a name="introduction1"></a>

CI/CD stands for Continuous Integration/Continuous Deployment or Delivery depending on who you talk to.

Source Code Repository is all the code required to build an application at any given point in time.

AWS Services that can help to deploy a CI/CD pipeline are as follows:
- CodeCommit
- CodeBuild 
- CodeDeploy
- CodePipeline

### Open Worldwide Application Security Project (OWASP) Top 10 C/CD Security Risks <a name="paragraph11"></a>

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

### Amazon CI/CD Pipeline – Security Best Practices – AWS <a name="paragraph12"></a>

-	Compliance standard is what your business requires from a CI/CD service and it is available in the region you need to operate in.
-	Amazon Organisations SCP – to restrict actions like creation, deletion, modification of production CI/CD pipeline services etc.
-	AWS CloudTrail is enabled & monitored to trigger alerts for malicious activities e.g. changes to Production CodePipeline etc.
-	GuardDuty is enabled for monitoring suspicious DNS comms (e.g. Crypto-mining etc) and automated for auto-remediation.
-	AWS Config Rules is enabled in the account and region of CodeBuild – conformance pack for any other CI/CD service.

### Amazon CI/CD Pipeline – Security Best Practices – Application <a name="paragraph13"></a>

-	Access Control – Roles or IAM Users for making changes in Amazon CICD services especially production related repositories, pipeline, build services etc.
-	Security of the CI/CD Pipeline – Source control, Secret Management, Container Registry, CI/CD Service (if not the AWS Service), IAM etc.
-	Security in the CI/CD Pipeline – Code Security Best Practices – SCA, SAST, Secret Scanner, DAST implemented in the CI/CD Pipeline.
-	Security of the CI/CD Pipeline entry points e.g. no bypass of CI/CD to make production changes.
-	Enable Encryption in Transit using TLS/SSL certification e.g. HTTPS
-	Only use Trusted Source Control for sending changes to CI/CD Pipeline
-	Develop process for continuously verifying if there is a change that may compromise the known state of a CI/CD Pipeline.   





