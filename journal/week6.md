# Week 6 — Deploying Containers

## Required Homework 

## Amazon ECS Security Best Practices

### Table of contents
- [Container Security Status in 2022](#introduction)
- [Container Services in AWS](#paragraph1)
- [Types of Launch Type to AWS](#paragraph2)
- [Shared Risk with AWS ECS](#ubparagraph3)
    1. [Sharing Responsibilities in a managed service model](#subparagraph1)

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

