# Week 6 — Deploying Containers

## Required Homework 

## Amazon ECS Security Best Practices

### Table of contents
- [Container Security Status in 2022](#ContainerSecurityStatusin2022)

[Container Services in AWS](#Container Services in AWS)
[Types of Launch Type to AWS](#Types of Launch Type to AWS)
[Shared Risk with AWS ECS](#Shared Risk with AWS ECS)
    1. [Sharing Responsibilities in a managed service model](#Sharing Responsibilities in a managed service model)

### Container Security Status in 2022 <a name="ContainerSecurityStatusin2022"></a>

- 75% of containers run with "high" or "critical" vulnerabilities
- 50% of containers have no limits defined
- 76% of containers run as root

### Container Services in AWS

-	Virtual Machine
-	ECS, Fargate, EKS

### Types of Launch Type to AWS

- Amazon EC2 architecture: This includes Elastic Load Balancing (ELB), Auto Scaling groups and Amazon EC2 instances.
-	Amazon ECS architecture: This includes Elastic Load Balancing (ELB), Amazon ECS cluster, Auto Scaling groups and Amazon EC2 instances.
-	ECS Fargate: This includes Elastic Load Balancing (ELB), Amazon ECS cluster and Fargate tasks.

### Shared Risk with AWS ECS

#### Sharing Responsibilities in a managed service model

**Traditional ECS instances**

| **User Manages**     | **AWS Manages** | 
| :---        |    :----:   |          
|Containerized Applications      | Virtual Machine       | 
|Container Runtime  | Physical Server        | 
|Storage, Logging, Monitoring Plugins      |        | 
|Operating System |         | 

