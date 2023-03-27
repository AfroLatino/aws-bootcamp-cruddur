# Week 6 — Deploying Containers

## Required Homework 

## Amazon ECS Security Best Practices

### Table of contents
- [Container Security Status in 2022](#introduction)
- [Container Services in AWS](#paragraph1)
- [Types of Launch Type to AWS](#paragraph2)
- [Shared Risk with AWS ECS](#paragraph3)
    - [Sharing Responsibilities in a managed service model](#subparagraph1)

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

### Security Challenges with AWS Fargate
- No visibility of Infrastructure
- Ephemeral Resources makes it hard to do triage or Forensics for detected threats
- No file/network monitoring
- Cannot run traditional Security Agents in Fargate
- User can run unverified Container images
- Containers can run as root and even with elevated privileges

### Amazon ECS (EC2) Setup 
If building a machine with containers, images are needed.

Then navigate to Elastic Container Registry (ECR) on AWS.

#### Creating a Repository
- In creating a repository owned by a company, security best practice would be to choose private visibility settings
- Enable tag immutability
- Enable Scan on push
- Enable KMS encryption

After creating ECR, the application will be created in Amazon Elastic Container Service.

#### Amazon Elastic Container Service
- Create cluster
- Create Amazon EC2 instances 
       - You'd choose a minimum of 1 and maximum of 2 desired capacity. 
       - Choose Amazon Linux 2 for Operating system/Architecture.
       -  Choose t2.micro as EC2 instance type.
       - SSH Key Pair should be none 
- Add tags – It is always a good practice to add tags.
- Create new task definition on ECS

#### Amazon ECR Images Security
- This is linked to Amazon Inspector
- It is using Synk in the background to find vulnerabilities

### Amazon ECS – Security Best Practices – AWS
- Cloud Control Plane Configuration – Access Control, Container Images etc
- Choosing the right Public or Private ECR for Images
- Amazon ECR Scan Images to "Scan on Push" using Basic or Enhanced (Inspector + Synk)
- Use VPC Endpoints or Security Groups with known sources only.
- Compliance standard is what your business requires.
- Amazon Organisations SCP – To manage ECS Task deletion, ECS creation, region lock etc.
- AWS CloudTrail is enabled & monitored to trigger alerts on malicious ECS behaviour by an identity in AWS.

### Amazon ECS – Security Best Practices – Application

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







