# Week 6 — Deploying Containers

## Required Homework 

## Amazon ECS Security Best Practices

### Table of contents
- [Container Security Status in 2022](#ContainerSecurityStatusin2022)

- [Container Services in AWS](#ContainerServicesinAWS)

- [Types of Launch Type to AWS](#TypesofLaunchTypetoAWS)

- [Shared Risk with AWS ECS](#SharedRiskwithAWSECS)
    1. [Sharing Responsibilities in a managed service model](#SharingResponsibilitiesinamanagedservicemodel)

### Container Security Status in 2022 <a name="ContainerSecurityStatusin2022"></a>

- 75% of containers run with "high" or "critical" vulnerabilities
- 50% of containers have no limits defined
- 76% of containers run as root

### Container Services in AWS <a name="ContainerServicesinAWS"></a>

-	Virtual Machine
-	ECS, Fargate, EKS

### Types of Launch Type to AWS <a name="TypesofLaunchTypetoAWS"></a>

- Amazon EC2 architecture: This includes Elastic Load Balancing (ELB), Auto Scaling groups and Amazon EC2 instances.
-	Amazon ECS architecture: This includes Elastic Load Balancing (ELB), Amazon ECS cluster, Auto Scaling groups and Amazon EC2 instances.
-	ECS Fargate: This includes Elastic Load Balancing (ELB), Amazon ECS cluster and Fargate tasks.

### Shared Risk with AWS ECS <a name="SharedRiskwithAWSECS"></a>

#### Sharing Responsibilities in a managed service model <a name="SharingResponsibilitiesinamanagedservicemodel"></a>

**Traditional ECS instances**

| **User Manages**     | **AWS Manages** | 
| :---        |    :----:   |          
|Containerized Applications      | Virtual Machine       | 
|Container Runtime  | Physical Server        | 
|Storage, Logging, Monitoring Plugins      |        | 
|Operating System |         | 

