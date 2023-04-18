# Week 9 — CI/CD with CodePipeline, CodeBuild and CodeDeploy

## Required Homework 

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





