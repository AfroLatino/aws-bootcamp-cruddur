# Week 10 & 11 — CloudFormation Part 1 & Part 2

## Required Homework 

## Table of contents
- [Introduction](#introduction)
- [Creating CloudFormation Stack](#paragraph1)
    - [Task Definition Guard File](#subparagraph1)
    - [CFN Guard RuleGen](#subparagraph2)
- [CFN for Networking Layer](#paragraph2)
- [CFN Diagramming the Network Layer](#paragraph3)
- [CFN Cluster Layer](#paragraph4)


### Introduction <a name="introduction"></a>

AWS CloudFormation is a service that helps you model and set up your AWS resources so that you can spend less time managing those resources and more time focusing on your applications that run in AWS.

When you use AWS CloudFormation, you work with templates and stacks. You create templates to describe your AWS resources and their properties. Whenever you create a stack, CloudFormation provisions the resources that are described in your template.

Reference:

[Amazon Docs - Cloud Formation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-whatis-concepts.html)


### Creating CloudFormation Stack <a name="paragraph1"></a>

Create a folder within aws called cfn. Then, create a file called template.yaml with the command below:

```sh
AWSTemplateFormatVersion: 2010-09-09
Description: |
  Setup ECS Cluster
Resources:
  ECSCluster:
     Type: 'AWS::ECS::Cluster'
```

Create a folder within bin called cfn. Then, create a file called networking-deploy.

```sh
#! /usr/bin/env bash

set -e # stop the execution of the script if it fails
	

CFN_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/template.yaml"

aws cloudformation deploy \
  --stack-name "my-cluster" \
  --template-file "$CFN_PATH" \
  --no-execute-changeset \
  --capabilities CAPABILITY_NAMED_IAM
```

This creates **my-cluster** stack.

```--no-execute-changeset``` is used so one could review what is being changed on the AWS Management Console.

You have to click on the **Change sets** section, then click on **Name -> Execute change set** using the default setting.


I amended template.yaml to include Properties of MyCluster as seen below:

```sh
AWSTemplateFormatVersion: 2010-09-09
Description: |
  Setup ECS Cluster
Resources:
  ECSCluster:
     Type: 'AWS::ECS::Cluster'
     Properties: 
       ClusterName: MyCluster
```

Then, ran ```./bin/cfn/networking-deploy``` 

This shows Modify as seen below:

![modifyCloudFormation](https://user-images.githubusercontent.com/78261965/234702423-b004d430-56f0-4f72-a0c7-013e1f3747e0.png)

Below is the CLI command for validating CloudFormation template:

```sh
aws cloudformation validate-template --template-body file:///workspace/aws-bootcamp-cruddur-2023/aws/cfn/template.yaml
```

Use cfn-lint to validate your templates, so insatll cfn-lint using the command below:

```sh
pip install cfn-lint
```

#### Task Definition Guard File <a name="subparagraph1"></a>

Create a task definition guard file via this path: ```aws/cfn/task-definition.guard``` using the command below:

```sh
aws_ecs_cluster_configuration {
  rules = [
    {
      rule = "task_definition_encryption"
      description = "Ensure task definitions are encrypted"
      level = "error"
      action {
        type = "disallow"
        message = "Task definitions in the Amazon ECS cluster must be encrypted"
      }
      match {
        type = "ecs_task_definition"
        expression = "encrypt == false"
      }
    },
    {
      rule = "network_mode"
      description = "Ensure Fargate tasks use awsvpc network mode"
      level = "error"
      action {
        type = "disallow"
        message = "Fargate tasks in the Amazon ECS cluster must use awsvpc network mode"
      }
      match {
        type = "ecs_task_definition"
        expression = "network_mode != 'awsvpc'"
      }
    },
    {
      rule = "execution_role"
      description = "Ensure Fargate tasks have an execution role"
      level = "error"
      action {
        type = "disallow"
        message = "Fargate tasks in the Amazon ECS cluster must have an execution role"
      }
      match {
        type = "ecs_task_definition"
        expression = "execution_role == null"
      }
    },
  ]
}
```

Then, run ```cargo install cfn-guard```

Add the below comands to the gitpod.yml file:

```sh
- name: cfn
  before: |
   pip install cfn-lint
   cargo install cfn-guard
```


#### CFN Guard RuleGen <a name="subparagraph2"></a>

Takes a JSON- or YAML-formatted AWS CloudFormation template file and autogenerates a set of AWS CloudFormation Guard rules that match the properties of the template resources. This command is a useful way to get started with rule writing or to create ready-to-use rules from known good templates.

You can run this - ```cfn-guard rulegen --template /workspace/aws-bootcamp-cruddur-2023/aws/cfn/template.yaml```

Reference:

[Amazon Docs - CFN Guard RuleGen](https://docs.aws.amazon.com/cfn-guard/latest/ug/cfn-guard-rulegen.html)


### CFN for Networking Layer <a name="paragraph2"></a>


### CFN Diagramming the Network Layer <a name="paragraph3"></a>

I used Lucid Chart for the diagram.

In order to get this working, I had to make 2 amendments on the File -> Page Settings as follows:

- Page -> Page Settings -> Canvas -> Ticked the box for Infinite canvas

- Page -> Page Settings -> Line settings -> Ticked the box for Show line jumps

I made a few changes to rectangle as follows:

-	Got rid of rounding in rectangles by choosing a rectangle shape from the Flowchart. Clicked on **Shape Options** -> Amended **ROUNDED** to 0 px
   
-	Right clicked on the Rectangle -> **Arrange** -> **Send to Back**

- Used the line colour of **#b0084d** to highlight the rectangle borders and CruddurStack & CruddurNetworking

- Got rid of padding by clicking on **Text Options** -> amended **PADDING** to 0cm


Please find below the screenshot of my CFN Diagramming the Network Layer:

![CFNdiagramming](https://user-images.githubusercontent.com/78261965/234646292-bfcd7c75-e7b7-491e-b4d0-7d846a99313c.png)

[Lucid Sharelink](https://lucid.app/lucidchart/56fb0dce-8f55-46ef-b05a-c33514c5b721/edit?viewport_loc=-1163%2C-115%2C3091%2C1309%2C0_0&invitationId=inv_dc84d8ea-5144-440c-87db-46fa390dcd24)


### CFN Cluster Layer <a name="paragraph4"></a>
