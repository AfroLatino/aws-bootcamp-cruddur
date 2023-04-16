# Week 8 — Serverless Image Processing

## Required Homework 

### Implement CDK Stack

The cdk pipeline called thumbing-serverless-cdk was added to the top level directory using the command below:

```sh
cd /workspace/aws-bootcamp-cruddur-2023
mkdir thumbing-serverless-cdk
```

The CDK Stack was installed globally using the AWS CDK CLI below:

```sh
npm install aws-cdk -g
```

The install was added to my gitpod task file using the command below:

```sh
- name: cdk
  before: |
   npm install aws-cdk -g
```

### Initialize a new project

A new cdk project was initialized within the folder we created below:

```sh
cdk init app --language typescript
```
      
