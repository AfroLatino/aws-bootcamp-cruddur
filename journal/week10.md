# Week 10 & 11 — CloudFormation Part 1 & Part 2

## Required Homework 

## Table of contents
- [Introduction](#introduction)
- [Creating CloudFormation Stack](#paragraph1)
    - [Task Definition Guard File](#subparagraph1)
    - [CFN Guard RuleGen](#subparagraph2)
    - [Create s3 bucket](#subparagraph3)
- [CFN for Networking Layer](#paragraph2)
    - [Components of CFN Networking Template File](#subparagraph4)
    - [Fixing !RefYAML error](#subparagraph5)
- [CFN Diagramming the Network Layer](#paragraph3)
- [CFN Cluster Layer](#paragraph4)
    - [Create Config Toml files](#subparagraph6)
- [CFN Service Layer](#paragraph5)
    - [Create Config Toml files](#subparagraph7)
    - [Create ECS Service](#subparagraph8)
    - [CFN Relational Database Service (RDS)](#subparagraph9)
- [SAM CFN for DynamoDB Streams Lambda](#paragraph6)
    - [Create Config Toml files](#subparagraph10)
    - [Create Build, Deploy, Package and Template files](#subparagraph11)
- [CFN CICD](#paragraph7) 
    - [Create Config Toml file](#subparagraph12)
    - [Create Template file](#subparagraph13)
    - [Create CodeBuild file](#subparagraph14)
- [CFN Static Website Hosting Frontend](#paragraph8) 

    
## Stretch Homework Challenges

## Table of contents

- [Retrieving Load Balancer IPs via AWS CLI](#paragraph9)
- [Retrieving Relational Database Service (RDS) IPs via AWS CLI](#paragraph10)
- [Retrieving AWS Elastic Beanstalk Public IPs via AWS CLI](#paragraph11)


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


#### Create s3 bucket <a name="subparagraph3"></a>

- Search for s3 in AWS Services, then click on s3
- Click on **Create bucket**
- Enter **cfn-artifacts-afrolatino** as the **Bucket name**. The bucket name must be unique.
- **AWS Region** is automatically populated
- Leave the default setting of **Default encryption**
- Then click on **Create bucket**

Then, modify the netwporking-deploy script by adding the s3-bucket just created as seen below:

```sh
#! /usr/bin/env bash

set -e # stop the execution of the script if it fails
	
CFN_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/template.yaml"

aws cloudformation deploy \
  --stack-name "cfn-artifacts-afrolatino" \
   --s3-bucket $CFN_BUCKET \
  --template-file "$CFN_PATH" \
  --no-execute-changeset \
  --capabilities CAPABILITY_NAMED_IAM
```

Then, run deploy by running ```./bin/cfn/deploy```

Please see the screenshot of the s3 bucket created below:

![cfn-artifacts-afrolatino](https://user-images.githubusercontent.com/78261965/234714835-87bbc6f9-0306-4258-849e-3ed12d462fe2.png)


### CFN for Networking Layer <a name="paragraph2"></a>

Before you run any templates, be sure to create an S3 bucket to contain all of the artifacts for CloudFormation as follows:

```sh
aws s3 mk s3://cfn-artifacts-afrolatino
export CFN_BUCKET="cfn-artifacts-afrolatino"
gp env CFN_BUCKET="cfn-artifacts-afrolatino"
```

Note: Bucket names are unique to each individual

Create a folder within aws/cfn called networking. Then, create a file called template.yaml with the command below:

```sh
AWSTemplateFormatVersion: 2010-09-09
Description: |
  The base networking components for our stack:
  - VPC
    - sets DNS hostnames for EC2 instances
    - Only IPV4, IPV6 is disabled
  - InternetGateway
  - Route Table
    - route to the IGW
    - route to Local
  - 6 Subnets Explicity Associated to Route Table
    - 3 Public Subnets numbered 1 to 3
    - 3 Private Subnets numbered 1 to 3
Parameters:
  VpcCidrBlock:
    Type: String
    Default: 10.0.0.0/16
  Az1:
    Type: AWS::EC2::AvailabilityZone::Name
    Default: $AWS_DEFAULT_REGIONa
  SubnetCidrBlocks: 
    Description: "Comma-delimited list of CIDR blocks for our private public subnets"
    Type: CommaDelimitedList
    Default: >
      10.0.0.0/24, 
      10.0.4.0/24, 
      10.0.8.0/24, 
      10.0.12.0/24,
      10.0.16.0/24,
      10.0.20.0/24
  Az2:
    Type: AWS::EC2::AvailabilityZone::Name
    Default: $AWS_DEFAULT_REGIONb
  Az3:
    Type: AWS::EC2::AvailabilityZone::Name
    Default: $AWS_DEFAULT_REGIONc
Resources:
  VPC:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc.html
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: !Ref VpcCidrBlock
      EnableDnsHostnames: true
      EnableDnsSupport: true
      InstanceTenancy: default
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}VPC"
  IGW:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-internetgateway.html
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}IGW"
  AttachIGW:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      VpcId: !Ref VPC
      InternetGatewayId: !Ref IGW
  RouteTable:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-routetable.html
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId:  !Ref VPC
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}RT"
  RouteToIGW:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-route.html
    Type: AWS::EC2::Route
    DependsOn: AttachIGW
    Properties:
      RouteTableId: !Ref RouteTable
      GatewayId: !Ref IGW
      DestinationCidrBlock: 0.0.0.0/0
  SubnetPub1:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet.html
    Type: AWS::EC2::Subnet
    Properties:
      AvailabilityZone: !Ref Az1
      CidrBlock: !Select [0, !Ref SubnetCidrBlocks]
      EnableDns64: false
      MapPublicIpOnLaunch: true #public subnet
      VpcId: !Ref VPC
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}SubnetPub1"
  SubnetPub2:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet.html
    Type: AWS::EC2::Subnet
    Properties:
      AvailabilityZone: !Ref Az2
      CidrBlock: !Select [1, !Ref SubnetCidrBlocks]
      EnableDns64: false
      MapPublicIpOnLaunch: true #public subnet
      VpcId: !Ref VPC
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}SubnetPub2"
  SubnetPub3:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet.html
    Type: AWS::EC2::Subnet
    Properties:
      AvailabilityZone: !Ref Az3
      CidrBlock: !Select [2, !Ref SubnetCidrBlocks]
      EnableDns64: false
      MapPublicIpOnLaunch: true #public subnet
      VpcId: !Ref VPC
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}SubnetPub3"
  SubnetPriv1:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet.html
    Type: AWS::EC2::Subnet
    Properties:
      AvailabilityZone: !Ref Az1
      CidrBlock: !Select [3, !Ref SubnetCidrBlocks]
      EnableDns64: false
      MapPublicIpOnLaunch: false #public subnet
      VpcId: !Ref VPC
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}SubnetPriv1"
  SubnetPriv2:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet.html
    Type: AWS::EC2::Subnet
    Properties:
      AvailabilityZone: !Ref Az2
      CidrBlock: !Select [4, !Ref SubnetCidrBlocks]
      EnableDns64: false
      MapPublicIpOnLaunch: false #public subnet
      VpcId: !Ref VPC
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}SubnetPriv2"
  SubnetPriv3:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet.html
    Type: AWS::EC2::Subnet
    Properties:
      AvailabilityZone: !Ref Az3
      CidrBlock: !Select [5, !Ref SubnetCidrBlocks]
      EnableDns64: false
      MapPublicIpOnLaunch: false #public subnet
      VpcId: !Ref VPC
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}SubnetPriv3"
  SubnetPub1RTAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref SubnetPub1
      RouteTableId: !Ref RouteTable
  SubnetPub2RTAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref SubnetPub2
      RouteTableId: !Ref RouteTable
  SubnetPub3RTAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref SubnetPub3
      RouteTableId: !Ref RouteTable
  SubnetPriv1RTAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref SubnetPriv1
      RouteTableId: !Ref RouteTable
  SubnetPriv2RTAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref SubnetPriv2
      RouteTableId: !Ref RouteTable
  SubnetPriv3RTAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref SubnetPriv3
      RouteTableId: !Ref RouteTable
Outputs:
  VpcId:
    Value: !Ref VPC
    Export:
      Name: !Sub "${AWS::StackName}VpcId"
  VpcCidrBlock:
    Value: !GetAtt VPC.CidrBlock
    Export:
      Name: !Sub "${AWS::StackName}VpcCidrBlock"
  SubnetCidrBlocks:
    Value: !Join [",", !Ref SubnetCidrBlocks]
    Export:
      Name: !Sub "${AWS::StackName}SubnetCidrBlocks"
  SubnetIds:
    Value: !Join 
      - ","
      - - !Ref SubnetPub1
        - !Ref SubnetPub2
        - !Ref SubnetPub3
        - !Ref SubnetPriv1
        - !Ref SubnetPriv2
        - !Ref SubnetPriv3
    Export:
      Name: !Sub "${AWS::StackName}SubnetIds"
  AvailabilityZones:
    Value: !Join 
      - ","
      - - !Ref Az1
        - !Ref Az2
        - !Ref Az3
    Export:
      Name: !Sub "${AWS::StackName}AvailabilityZones"
```

Amend ```bin/cfn/networking-deploy``` to the command below:

```sh
#! /usr/bin/env bash
set -e # stop the execution of the script if it fails

CFN_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/networking/template.yaml"
echo $CFN_PATH

cfn-lint $CFN_PATH

aws cloudformation deploy \
  --stack-name "CrdNet" \
  --s3-bucket $CFN_BUCKET \
  --template-file "$CFN_PATH" \
  --no-execute-changeset \
  --tags group=cruddur-networking \
  --capabilities CAPABILITY_NAMED_IAM
```

Then run the commands below within aws-bootcamp-cruddur-2023/thumbing-serverless-cdk:

```sh
export CFN_BUCKET="cfn-artifacts-afrolatino"
gp env CFN_BUCKET="cfn-artifacts-afrolatino"
```

Then, return to the main branch and run the command below:
```./bin/cfn/networking-deploy```

- Then, go over to CloudFormation and refresh the screen.

- Navigate to **Change sets** section, then **Execute change set**

A CloudFormation of **CrdNet** is created as seen below:

![CrdNet CloudFormation](https://user-images.githubusercontent.com/78261965/234980574-fcb56c64-65f7-4f6d-82fc-343a1cb043d7.png)


#### Components of CFN Networking Template File <a name="subparagraph4"></a>

- Description
- Parameters used are as follows:
  - VpcCidrBlock
  - Az1
  - SubnetCidrBlocks
  - Az2
  - Az3
- Resources used are as follows:
  - Virtual Private Connection (VPC)
  - Internet Gateway (IGW)
  - Attach Internet Gateway (AttachIGW)
  - RouteTable
  - RouteToInternetGateway (IGW)
  - SubnetPub1
  - SubnetPub2
  - SubnetPub3
  - SubnetPriv1
  - SubnetPriv2
  - SubnetPriv3
  - SubnetPub1RTAssociation
  - SubnetPub2RTAssociation
  - SubnetPub3RTAssociation
  - SubnetPriv1RTAssociation
  - SubnetPriv2RTAssociation
  - SubnetPriv3RTAssociation
- Outputs used are as follows:
  - VpcId
  - VpcCidrBlock
  - SubnetCidrBlocks
  - SubnetIds
  - AvailabilityZones


Difference between Public Subnet (SubnetPub) and Private Subnet (SubnetPriv) is that **MapPublicIpOnLaunch** is *true* for **Public Subnet** and *false* for **Private Subnet**.


#### Fixing !RefYAML error <a name="subparagraph5"></a>

Navigate to **Settings** in Gitpod, search for YAML, Yaml: Custom Tags -> Edit in **settings.json**,  and add the below to **"yaml.customTags"**

```yaml
"yaml.customTags": [
        "!Equals sequence",
        "!FindInMap sequence",
        "!GetAtt",
        "!GetAZs",
        "!ImportValue",
        "!Join sequence",
        "!Ref",
        "!Select sequence",
        "!Split sequence",
        "!Sub"
      ]   
```


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

![CFN-diagram-latest](https://github.com/AfroLatino/aws-bootcamp-cruddur-2023/assets/78261965/54823319-05d7-418a-a6ee-7a726bc07f0d)

[Lucid Sharelink](https://lucid.app/lucidchart/f75c2844-ebe9-4b86-b34f-4a6a7ca45933/edit?viewport_loc=-2639%2C-577%2C5616%2C2413%2C0_0&invitationId=inv_459df47d-2f9f-4c85-b6be-0cbbb06c4805)


### CFN Cluster Layer <a name="paragraph4"></a>

Create a folder within aws/cfn called cluster. Then, create a file called ```template.yaml``` as seen below:

```sh
AWSTemplateFormatVersion: 2010-09-09

Description: |
  The networking and cluster configuration to support fargate containers
  - ECS Fargate Cluster
  - Application Load Balanacer (ALB)
    - ipv4 only
    - internet facing
    - certificate attached from Amazon Certification Manager (ACM)
  - ALB Security Group
  - HTTPS Listerner
    - send naked domain to frontend Target Group
    - send api. subdomain to backend Target Group
  - HTTP Listerner
    - redirects to HTTPS Listerner
  - Backend Target Group
  - Frontend Target Group
Parameters:
  NetworkingStack:
    Type: String
    Description: This is our base layer of networking components eg. VPC, Subnets
    Default: CrdNet
  CertificateArn:
    Type: String
  #Frontend ------
  FrontendPort:
    Type: Number
    Default: 3000
  FrontendHealthCheckIntervalSeconds:
    Type: Number
    Default: 15
  FrontendHealthCheckPath:
    Type: String
    Default: "/"
  FrontendHealthCheckPort:
    Type: String
    Default: 80
  FrontendHealthCheckProtocol:
    Type: String
    Default: HTTP
  FrontendHealthCheckTimeoutSeconds:
    Type: Number
    Default: 5
  FrontendHealthyThresholdCount:
    Type: Number
    Default: 2
  FrontendUnhealthyThresholdCount:
    Type: Number
    Default: 2
  #Backend ------
  BackendPort:
    Type: Number
    Default: 4567
  BackendHealthCheckIntervalSeconds:
    Type: String
    Default: 15
  BackendHealthCheckPath:
    Type: String
    Default: "/api/health-check"
  BackendHealthCheckPort:
    Type: String
    Default: 80
  BackendHealthCheckProtocol:
    Type: String
    Default: HTTP
  BackendHealthCheckTimeoutSeconds:
    Type: Number
    Default: 5
  BackendHealthyThresholdCount:
    Type: Number
    Default: 2
  BackendUnhealthyThresholdCount:
    Type: Number
    Default: 2
Resources:
  FargateCluster:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-cluster.html
    Type: AWS::ECS::Cluster
    Properties:
      ClusterName: !Sub "${AWS::StackName}FargateCluster"
      CapacityProviders:
        - FARGATE
      ClusterSettings:
        - Name: containerInsights
          Value: enabled
      Configuration:
        ExecuteCommandConfiguration:
          # KmsKeyId: !Ref KmsKeyId
          Logging: DEFAULT
      ServiceConnectDefaults:
        Namespace: cruddur
  ALB:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties: 
      Name: !Sub "${AWS::StackName}ALB"
      Type: application
      IpAddressType: ipv4
      # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-loadbalancerattributes.html
      Scheme: internet-facing
      SecurityGroups:
        - !GetAtt ALBSG.GroupId
      Subnets:
        Fn::Split:
          - ","
          - Fn::ImportValue:
              !Sub "${NetworkingStack}PublicSubnetIds"
      LoadBalancerAttributes:
        - Key: routing.http2.enabled
          Value: true
        - Key: routing.http.preserve_host_header.enabled
          Value: false
        - Key: deletion_protection.enabled
          Value: true
        - Key: load_balancing.cross_zone.enabled
          Value: true
        - Key: access_logs.s3.enabled
          Value: false
        # In-case we want to turn on logs
        # - Name: access_logs.s3.bucket
        #   Value: bucket-name
        # - Name: access_logs.s3.prefix
        #   Value: ""
  HTTPSListener:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
      Protocol: HTTPS
      Port: 443
      LoadBalancerArn: !Ref ALB
      Certificates: 
        - CertificateArn: !Ref CertificateArn
      DefaultActions:
        - Type: forward
          TargetGroupArn:  !Ref FrontendTG
  HTTPListener:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
        Protocol: HTTP
        Port: 80
        LoadBalancerArn: !Ref ALB
        DefaultActions:
          - Type: redirect
            RedirectConfig:
              Protocol: "HTTPS"
              Port: 443
              Host: "#{host}"
              Path: "/#{path}"
              Query: "#{query}"
              StatusCode: "HTTP_301"
  ApiALBListernerRule:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html
    Type: AWS::ElasticLoadBalancingV2::ListenerRule
    Properties:
      Conditions: 
        - Field: host-header
          HostHeaderConfig: 
            Values: 
              - api.cruddur.com
      Actions: 
        - Type: forward
          TargetGroupArn:  !Ref BackendTG
      ListenerArn: !Ref HTTPSListener
      Priority: 1
  ALBSG:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group.html
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: !Sub "${AWS::StackName}AlbSG"
      GroupDescription: Public Facing SG for our Cruddur ALB
      VpcId:
        Fn::ImportValue:
          !Sub ${NetworkingStack}VpcId
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: '0.0.0.0/0'
          Description: INTERNET HTTPS
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: '0.0.0.0/0'
          Description: INTERNET HTTP
  BackendTG:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      #Name: !Sub "${AWS::StackName}BackendTG"
      Port: !Ref BackendPort
      HealthCheckEnabled: true
      HealthCheckProtocol: !Ref BackendHealthCheckProtocol
      HealthCheckIntervalSeconds: !Ref BackendHealthCheckIntervalSeconds
      HealthCheckPath: !Ref BackendHealthCheckPath
      HealthCheckPort: !Ref BackendHealthCheckPort
      HealthCheckTimeoutSeconds: !Ref BackendHealthCheckTimeoutSeconds
      HealthyThresholdCount: !Ref BackendHealthyThresholdCount
      UnhealthyThresholdCount: !Ref BackendUnhealthyThresholdCount
      IpAddressType: ipv4
      Matcher: 
        HttpCode: 200
      Protocol: HTTP
      ProtocolVersion: HTTP2
      TargetType: ip
      TargetGroupAttributes: 
        - Key: deregistration_delay.timeout_seconds
          Value: 0
      VpcId:
        Fn::ImportValue:
          !Sub ${NetworkingStack}VpcId
      Tags:
        - Key: target-group-name
          Value: backend
  FrontendTG:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      #Name: !Sub "${AWS::StackName}FrontendTG"
      Port: !Ref FrontendPort
      HealthCheckEnabled: true
      HealthCheckProtocol: !Ref FrontendHealthCheckProtocol
      HealthCheckIntervalSeconds: !Ref FrontendHealthCheckIntervalSeconds
      HealthCheckPath: !Ref FrontendHealthCheckPath
      HealthCheckPort: !Ref FrontendHealthCheckPort
      HealthCheckTimeoutSeconds: !Ref FrontendHealthCheckTimeoutSeconds
      HealthyThresholdCount: !Ref FrontendHealthyThresholdCount
      UnhealthyThresholdCount: !Ref FrontendUnhealthyThresholdCount
      IpAddressType: ipv4
      Matcher: 
        HttpCode: 200
      Protocol: HTTP
      ProtocolVersion: HTTP2
      TargetType: ip
      TargetGroupAttributes: 
        - Key: deregistration_delay.timeout_seconds
          Value: 0
      VpcId:
        Fn::ImportValue:
          !Sub ${NetworkingStack}VpcId
      Tags:
        - Key: target-group-name
          Value: frontend
Outputs:
  ClusterName:
    Value: !Ref FargateCluster
    Export:
      Name: !Sub "${AWS::StackName}ClusterName"
  ALBSecurityGroupId:
    Value: !GetAtt ALBSG.GroupId
    Export:
      Name: !Sub "${AWS::StackName}ALBSecurityGroupId"
  FrontendTGArn:
    Value: !Ref FrontendTG
    Export:
      Name: !Sub "${AWS::StackName}FrontendTGArn"
  BackendTGArn:
    Value: !Ref BackendTG
    Export:
      Name: !Sub "${AWS::StackName}BackendTGArn
```

Create a file within bin/cfn called ```cluster-deploy``` using the command below: 

```sh
#! /usr/bin/env bash
set -e # stop the execution of the script if it fails

CFN_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/cluster/template.yaml"
CONFIG_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/cluster/config.toml"
echo $CFN_PATH

cfn-lint $CFN_PATH

BUCKET=$(cfn-toml key deploy.bucket -t $CONFIG_PATH)
REGION=$(cfn-toml key deploy.region -t $CONFIG_PATH)
STACK_NAME=$(cfn-toml key deploy.stack_name -t $CONFIG_PATH)
PARAMETERS=$(cfn-toml params v2 -t $CONFIG_PATH)

aws cloudformation deploy \
  --stack-name $STACK_NAME \
  --s3-bucket $BUCKET \
  --region $REGION \
  --template-file "$CFN_PATH" \
  --no-execute-changeset \
  --tags group=cruddur-cluster \
  --parameter-overrides $PARAMETERS \
  --capabilities CAPABILITY_NAMED_IAM
```

Then, make this executable by running this command - ```chmod u+x ./bin/cfn/cluster-deploy```.

Then, run ```./bin/cfn/cluster-deploy```


#### Create Config Toml files <a name="subparagraph6"></a>

TOML (Tom's Obvious Minimal Language) is a configuration file format that is easy to read and write. It's minimal, and even people with no programming experience can easily understand it.

TOML supports many data structures, such as key-value pairs, arrays, and tables.

On the main directory, type ``gem install cfn-toml``` to install cfn-toml.

I also updated gitpod by adding the code below to the tasks:

```sh
gem install cfn-toml 
```

Added a file called config.toml to ```aws/cfn/cluster``` with the code below:

```sh
[deploy]
bucket = '$BUCKET_NAME'
region = '$AWS_DEFAUKT_REGION'
stack_name = '$STACK_NAME

[parameters]
CertificateArn = $CERTIFICATE_ARN'
NetworkingStack = 'CrdNet'
```

Added ```config/toml.example``` with the code below:

```sh
[deploy]
bucket = ''
region = ''
stack_name = ''

[parameters]
CertificateArn = ''
```

Within aws/cfn/networking, create config.toml file below:

```sh
[deploy]
bucket = '$BUCKET_NAME
region = '$AWS_DEFAULT_REGION'
stack_name = '$STACK_NAME'
```

Added ```config.toml.example``` with the code below:

```sh
[deploy]
bucket = ''
region = ''
stack_name = ''
```

Amended ```bin/cfn/networking-deploy``` to include cfn-toml as seen below:

```sh
#! /usr/bin/env bash
set -e # stop the execution of the script if it fails

CFN_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/networking/template.yaml"
CONFIG_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/networking/config.toml"
echo $CFN_PATH

cfn-lint $CFN_PATH

BUCKET=$(cfn-toml key deploy.bucket -t $CONFIG_PATH)
REGION=$(cfn-toml key deploy.region -t $CONFIG_PATH)
STACK_NAME=$(cfn-toml key deploy.stack_name -t $CONFIG_PATH)

aws cloudformation deploy \
  --stack-name $STACK_NAME \
  --s3-bucket $BUCKET \
  --region $REGION \
  --template-file "$CFN_PATH" \
  --no-execute-changeset \
  --tags group=cruddur-networking \
  --capabilities CAPABILITY_NAMED_IAM
```

Amended ```bin/cfn/cluster-deploy``` to include cfn-toml as seen below:

```sh
#! /usr/bin/env bash
set -e # stop the execution of the script if it fails

CFN_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/cluster/template.yaml"
CONFIG_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/cluster/config.toml"
echo $CFN_PATH

cfn-lint $CFN_PATH

BUCKET=$(cfn-toml key deploy.bucket -t $CONFIG_PATH)
REGION=$(cfn-toml key deploy.region -t $CONFIG_PATH)
STACK_NAME=$(cfn-toml key deploy.stack_name -t $CONFIG_PATH)
PARAMETERS=$(cfn-toml params v2 -t $CONFIG_PATH)

aws cloudformation deploy \
  --stack-name $STACK_NAME \
  --s3-bucket $BUCKET \
  --region $REGION \
  --template-file "$CFN_PATH" \
  --no-execute-changeset \
  --tags group=cruddur-cluster \
  --parameter-overrides $PARAMETERS \
  --capabilities CAPABILITY_NAMED_IAM
```

Then run the commands below to execute networking-deploy and cluster-deploy files:

```sh
./bin/cfn/networking-deploy
./bin/cfn/cluster-deploy
```

Find the screenshots below of the stacks created:

![allstackscreatedsuccessfully](https://user-images.githubusercontent.com/78261965/236584014-b67e6d61-62c1-4a13-9f71-abc1df0412ec.png)



### CFN Service Layer <a name="paragraph5"></a>

Create a new folder called ```service``` within ```aws/cfn``` using the command below:

```sh
AWSTemplateFormatVersion: 2010-09-09
Description: |
  Task Definition
  Fargate Service
  Execution Role
  Task Role

Parameters:
  NetworkingStack:
    Type: String
    Description: This is our base layer of networking components eg. VPC, Subnets
    Default: CrdNet
  ClusterStack:
    Type: String
    Description: This is our cluster layer eg. ECS Cluster, ALB
    Default: CrdCluster
  ContainerPort:
    Type: Number
    Default: 4567
  ServiceCpu:
    Type: String
    Default: '256'
  ServiceMemory:
    Type: String
    Default: '512'
  ServiceName:
    Type: String
    Default: backend-flask
  ContainerName:
    Type: String
    Default: backend-flask
  TaskFamily:
    Type: String
    Default: backend-flask
  EcrImage:
    Type: String
    Default: '$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/backend-flask'
  EnvOtelServiceName:
    Type: String
    Default: backend-flask
  EnvOtelExporterOtlpEndpoint:
    Type: String
    Default: https://api.honeycomb.io
  EnvAWSCognitoUserPoolId:
    Type: String
    Default: $AWS_COGNITO_USER_POOL_ID
  EnvCognitoUserPoolClientId:
    Type: String
    Default: $AWS_COGNITO_USER_POOL_CLIENT_ID
  EnvFrontendUrl:
    Type: String
    Default: "*"
  EnvBackendUrl:
    Type: String
    Default: "*"
  SecretsAWSAccessKeyId:
    Type: String
    Default: 'arn:aws:ssm:$AWS_DEFAULT_REGION:$AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/AWS_ACCESS_KEY_ID'
  SecretsSecretAccessKey:
    Type: String
    Default: 'arn:aws:ssm:$AWS_DEFAULT_REGION:$AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/AWS_SECRET_ACCESS_KEY'
  SecretsConnectionUrl:
    Type: String
    Default: 'arn:aws:ssm:$AWS_DEFAULT_REGION:$AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/CONNECTION_URL'
  SecretsRollbarAccessToken:
    Type: String
    Default: 'arn:aws:ssm:$AWS_DEFAULT_REGION:$AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/ROLLBAR_ACCESS_TOKEN'
  SecretsOtelExporterOltpHeaders:
    Type: String
    Default: 'arn:aws:ssm:$AWS_DEFAULT_REGION:$AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/OTEL_EXPORTER_OTLP_HEADERS'
  
Resources:
  FargateService:
  # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html
    Type: AWS::ECS::Service
    Properties:
      Cluster:
        Fn::ImportValue:
          !Sub "${ClusterStack}ClusterName"
      DeploymentController:
        Type: ECS
      DesiredCount: 1
      EnableECSManagedTags: true
      EnableExecuteCommand: true
      HealthCheckGracePeriodSeconds: 0
      LaunchType: FARGATE
      LoadBalancers:
        - TargetGroupArn:
            Fn::ImportValue:
              !Sub "${ClusterStack}BackendTGArn"
          ContainerName: 'backend-flask'
          ContainerPort: !Ref ContainerPort
      NetworkConfiguration:
        AwsvpcConfiguration:
          AssignPublicIp: ENABLED
          SecurityGroups:
            - Fn::ImportValue:
                !Sub "${ClusterStack}ServiceSecurityGroupId"
          Subnets:
            Fn::Split:
              - ","
              - Fn::ImportValue:
                  !Sub "${NetworkingStack}PublicSubnetIds"
      PlatformVersion: LATEST
      PropagateTags: SERVICE
      ServiceConnectConfiguration:
        Enabled: true
        Namespace: "cruddur"
        # TODO - If you want to log
        # LogConfiguration
        Services:
          - DiscoveryName: backend-flask
            PortName: backend-flask
            ClientAliases:
              - Port: !Ref ContainerPort
      #ServiceRegistries:
      #  - RegistryArn: !Sub 'arn:aws:servicediscovery:${AWS::Region}:${AWS::AccountId}:service/srv-cruddur-backend-flask'
      #    Port: !Ref ContainerPort
      #    ContainerName: 'backend-flask'
      #    ContainerPort: !Ref ContainerPort
      ServiceName: !Ref ServiceName
      TaskDefinition: !Ref TaskDefinition

  TaskDefinition:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html
    Type: 'AWS::ECS::TaskDefinition'
    Properties:
      Family: !Ref TaskFamily
      ExecutionRoleArn: !GetAtt ExecutionRole.Arn
      TaskRoleArn: !GetAtt TaskRole.Arn
      NetworkMode: 'awsvpc'
      Cpu: !Ref ServiceCpu
      Memory: !Ref ServiceMemory
      RequiresCompatibilities:
        - 'FARGATE'
      ContainerDefinitions:
        - Name: 'xray'
          Image: 'public.ecr.aws/xray/aws-xray-daemon'
          Essential: true
          User: '1337'
          PortMappings:
            - Name: 'xray'
              ContainerPort: 2000
              Protocol: 'udp'
        - Name: 'backend-flask'
          Image: !Ref EcrImage 
          Essential: true
          HealthCheck:
            Command:
              - 'CMD-SHELL'
              - 'python /backend-flask/bin/health-check'
            Interval: 30
            Timeout: 5
            Retries: 3
            StartPeriod: 60
          PortMappings:
            - Name: !Ref ContainerName
              ContainerPort: !Ref ContainerPort
              Protocol: 'tcp'
              AppProtocol: 'http'
          LogConfiguration:
            LogDriver: 'awslogs'
            Options:
              awslogs-group: 'cruddur'
              awslogs-region: !Ref AWS::Region
              awslogs-stream-prefix: !Ref ServiceName
          Environment:
            - Name: 'OTEL_SERVICE_NAME'
              Value: !Ref EnvOtelServiceName
            - Name: 'OTEL_EXPORTER_OTLP_ENDPOINT'
              Value: !Ref EnvOtelExporterOtlpEndpoint
            - Name: 'AWS_COGNITO_USER_POOL_ID'
              Value: !Ref EnvAWSCognitoUserPoolId
            - Name: 'AWS_COGNITO_USER_POOL_CLIENT_ID'
              Value: !Ref EnvCognitoUserPoolClientId
            - Name: 'FRONTEND_URL'
              Value: !Ref EnvFrontendUrl
            - Name: 'BACKEND_URL'
              Value: !Ref EnvBackendUrl
            - Name: 'AWS_DEFAULT_REGION'
              Value: !Ref AWS::Region
          Secrets:
            - Name: 'AWS_ACCESS_KEY_ID'
              ValueFrom: !Ref SecretsAWSAccessKeyId
            - Name: 'AWS_SECRET_ACCESS_KEY'
              ValueFrom: !Ref SecretsSecretAccessKey
            - Name: 'CONNECTION_URL'
              ValueFrom: !Ref SecretsConnectionUrl
            - Name: 'ROLLBAR_ACCESS_TOKEN'
              ValueFrom: !Ref SecretsRollbarAccessToken
            - Name: 'OTEL_EXPORTER_OTLP_HEADERS'
              ValueFrom: !Ref SecretsOtelExporterOltpHeaders
  ExecutionRole:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html
    Type: AWS::IAM::Role
    Properties:
      RoleName: CruddurServiceExecutionRole
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: 'Allow'
            Principal:
              Service: 'ecs-tasks.amazonaws.com'
            Action: 'sts:AssumeRole'
      Policies:
        - PolicyName: 'cruddur-execution-policy'
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Sid: 'VisualEditor0'
                Effect: 'Allow'
                Action:
                  - 'ecr:GetAuthorizationToken'
                  - 'ecr:BatchCheckLayerAvailability'
                  - 'ecr:GetDownloadUrlForLayer'
                  - 'ecr:BatchGetImage'
                  - 'logs:CreateLogStream'
                  - 'logs:PutLogEvents'
                Resource: '*'
              - Sid: 'VisualEditor1'
                Effect: 'Allow'
                Action:
                  - 'ssm:GetParameters'
                  - 'ssm:GetParameter'
                Resource: !Sub 'arn:aws:ssm:${AWS::Region}:${AWS::AccountId}:parameter/cruddur/${ServiceName}/*'
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/CloudWatchLogsFullAccess
  TaskRole:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html
    Type: AWS::IAM::Role
    Properties:
      RoleName: CruddurServiceTaskRole
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: 'Allow'
            Principal:
              Service: 'ecs-tasks.amazonaws.com'
            Action: 'sts:AssumeRole'
      Policies:
        - PolicyName: 'cruddur-task-policy'
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Sid: 'VisualEditor0'
                Effect: 'Allow'
                Action:
                  - ssmmessages:CreateControlChannel
                  - ssmmessages:CreateDataChannel
                  - ssmmessages:OpenControlChannel
                  - ssmmessages:OpenDataChannel
                Resource: '*'
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/CloudWatchLogsFullAccess
        - arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess
```

#### Create Config Toml files  <a name="subparagraph7"></a>
Create a file called ```aws/cfn/service/config.toml``` with the command below:

```sh
[deploy]
bucket = '$BUCKET_NAME
region = '$AWS_DEFAULT_REGION'
stack_name = '$STACK_NAME'
```

Create a file called ```aws/cfn/service/config.toml.example``` with the command below:

```sh
[deploy]
bucket = ''
region = ''
stack_name = ''
```

Add a file to deploy this template called ```service-deploy``` within ```bin\cfn``` with the command below:

```sh
#! /usr/bin/env bash
set -e # stop the execution of the script if it fails

CFN_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/service/template.yaml"
CONFIG_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/service/config.toml"
echo $CFN_PATH

cfn-lint $CFN_PATH

BUCKET=$(cfn-toml key deploy.bucket -t $CONFIG_PATH)
REGION=$(cfn-toml key deploy.region -t $CONFIG_PATH)
STACK_NAME=$(cfn-toml key deploy.stack_name -t $CONFIG_PATH)
#PARAMETERS=$(cfn-toml params v2 -t $CONFIG_PATH)

aws cloudformation deploy \
  --stack-name $STACK_NAME \
  --s3-bucket $BUCKET \
  --region $REGION \
  --template-file "$CFN_PATH" \
  --no-execute-changeset \
  --tags group=cruddur-backend-flask \
  --capabilities CAPABILITY_NAMED_IAM
  #--parameter-overrides $PARAMETERS \
```
Make this file executable using this command: ```chmod u+x ./bin/cfn/service-deploy```


#### Create ECS Service  <a name="subparagraph8"></a>

Create an ECS service and add this within ```bin/backend/create-service``` using the command below:

```sh
#! /usr/bin/bash

CLUSTER_NAME="CrdClusterFargateCluster"
SERVICE_NAME="backend-flask"
TASK_DEFINTION_FAMILY="backend-flask"


LATEST_TASK_DEFINITION_ARN=$(aws ecs describe-task-definition \
--task-definition $TASK_DEFINTION_FAMILY \
--query 'taskDefinition.taskDefinitionArn' \
--output text)

echo "TASK DEF ARN:"
echo $LATEST_TASK_DEFINITION_ARN

aws ecs create-service \
--cluster $CLUSTER_NAME \
--service-name $SERVICE_NAME \
--task-definition $LATEST_TASK_DEFINITION_ARN
```

#### CFN Relational Database Service (RDS)  <a name="subparagraph9"></a>

Create a new  file within ```aws/cfn/db``` called ```template``` using the command below:

```sh
AWSTemplateFormatVersion: 2010-09-09
Description: |
  The primary Postgres RDS Database for the application
  - RDS Instance
  - Database Security Group
  - DBSubnetGroup

Parameters:
  NetworkingStack:
    Type: String
    Description: This is our base layer of networking components eg. VPC, Subnets
    Default: CrdNet
  ClusterStack:
    Type: String
    Description: This is our FargateCluster
    Default: CrdCluster
  BackupRetentionPeriod:
    Type: Number
    Default: 0
  DBInstanceClass:
    Type: String
    Default: db.t4g.micro
  DBInstanceIdentifier:
    Type: String
    Default: cruddur-instance
  DBName:
    Type: String
    Default: cruddur
  DeletionProtection:
    Type: String
    AllowedValues:
      - true
      - false
    Default: true
  EngineVersion:
    Type: String
    #  DB Proxy only supports very specific versions of Postgres
    #  https://stackoverflow.com/questions/63084648/which-rds-db-instances-are-supported-for-db-proxy
    Default: '15.2'
  MasterUsername:
    Type: String
  MasterUserPassword:
    Type: String
    NoEcho: true
Resources:
  RDSPostgresSG:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group.html
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: !Sub "${AWS::StackName}RDSSG"
      GroupDescription: Public Facing SG for our Cruddur ALB
      VpcId:
        Fn::ImportValue:
          !Sub ${NetworkingStack}VpcId
      SecurityGroupIngress:
        - IpProtocol: tcp
          SourceSecurityGroupId:
            Fn::ImportValue:
              !Sub ${ClusterStack}ServiceSecurityGroupId
          FromPort: 5432
          ToPort: 5432
          Description: ALB HTTP
  DBSubnetGroup:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsubnetgroup.html
    Type: AWS::RDS::DBSubnetGroup
    Properties:
      DBSubnetGroupName: !Sub "${AWS::StackName}DBSubnetGroup"
      DBSubnetGroupDescription: !Sub "${AWS::StackName}DBSubnetGroup"
      SubnetIds: { 'Fn::Split' : [ ','  , { "Fn::ImportValue": { "Fn::Sub": "${NetworkingStack}PublicSubnetIds" }}] }
  Database:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html
    Type: AWS::RDS::DBInstance
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-deletionpolicy.html
    DeletionPolicy: 'Snapshot'
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatereplacepolicy.html
    UpdateReplacePolicy: 'Snapshot'
    Properties:
      AllocatedStorage: '20'
      AllowMajorVersionUpgrade: true
      AutoMinorVersionUpgrade: true
      BackupRetentionPeriod: !Ref  BackupRetentionPeriod
      DBInstanceClass: !Ref DBInstanceClass
      DBInstanceIdentifier: !Ref DBInstanceIdentifier
      DBName: !Ref DBName
      DBSubnetGroupName: !Ref DBSubnetGroup
      DeletionProtection: !Ref DeletionProtection
      EnablePerformanceInsights: true
      Engine: postgres
      EngineVersion: !Ref EngineVersion

# Must be 1 to 63 letters or numbers.
# First character must be a letter.
# Can't be a reserved word for the chosen database engine.
      MasterUsername:  !Ref MasterUsername
      # Constraints: Must contain from 8 to 128 characters.
      MasterUserPassword: !Ref MasterUserPassword
      PubliclyAccessible: true
      VPCSecurityGroups:
        - !GetAtt RDSPostgresSG.GroupId
```

Create a ```config.toml``` via ```/aws/cfn/db``` using the command below:

```sh
[deploy]
bucket = '$BUCKET_NAME'
region = '$AWS_DEFAULT_REGION'
stack_name = '$STACK_NAME'

[parameters]
NetworkingStack = 'CrdNet'
ClusterStack = 'CrdCluster'
MasterUsername = 'cruddurroot'
```

Create the deploy file within ```/bin/cfn/db-deploy``` using the command below:

```sh
#! /usr/bin/env bash
set -e # stop the execution of the script if it fails

CFN_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/db/template.yaml"
CONFIG_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/db/config.toml"
echo $CFN_PATH

cfn-lint $CFN_PATH

BUCKET=$(cfn-toml key deploy.bucket -t $CONFIG_PATH)
REGION=$(cfn-toml key deploy.region -t $CONFIG_PATH)
STACK_NAME=$(cfn-toml key deploy.stack_name -t $CONFIG_PATH)
PARAMETERS=$(cfn-toml params v2 -t $CONFIG_PATH)

aws cloudformation deploy \
  --stack-name $STACK_NAME \
  --s3-bucket $BUCKET \
  --region $REGION \
  --template-file "$CFN_PATH" \
  --no-execute-changeset \
  --tags group=cruddur-cluster \
  --parameter-overrides $PARAMETERS MasterUserPassword=$DB_PASSWORD \
  --capabilities CAPABILITY_NAMED_IAM
```

This creates a RDS database called **cruddur-instance**.

- Copy the endpoint from this database and copy unto parameter store.
- Navigate to Systems Manager on AWS Services Search
- Then search for parameter store
- Navigate to /cruddur/backend-flask/CONNECTION_URL. Check if the endpoint URL matches that of the RDS database. If not, continue with the steps below.
- Click on Edit
- Update Value after **password@** and before **:5432** to enter the endpoint.
- Then save changes

### SAM CFN for DynamoDB Streams Lambda <a name="paragraph6"></a>

Update gitpod file with the AWS SAM commands below:

```sh
tasks:
  - name: aws-sam
    init: |
      cd /workspace
      wget https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip
      unzip aws-sam-cli-linux-x86_64.zip -d sam-installation
      sudo ./sam-installation/install
      cd $THEIA_WORKSPACE_ROOT
 ```

#### Create Config Toml files <a name="subparagraph10">
	
Create a folder called ```ddb``` in the main directory, then add a file called ```config.toml``` with the command below:
	
```sh
version=0.1
[default.build.parameters]
region = "$AWS_DEFAULT_REGION"

[default.package.parameters]
region = "$AWS_DEFAULT_REGION"

[default.deploy.parameters]
region = "$AWS_DEFAULT_REGION"
```
	
#### Create Build, Deploy, Package and Template files <a name="subparagraph11">
	
Create a folder called ```ddb``` in the main directory, then add a file called ```template.yaml``` with the command below:

```sh
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: | 
  - DynamoDB Table
  - DynamoDB Stream
Parameters:
  PythonRuntime:
    Type: String
    Default: python3.9
  MemorySize:
    Type: String
    Default:  128
  Timeout:
    Type: Number
    Default: 3
  DeletionProtectionEnabled:
    Type: String
    Default: false
Resources:
  DynamoDBTable:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html
    Type: AWS::DynamoDB::Table
    Properties: 
      AttributeDefinitions: 
        - AttributeName: message_group_uuid
          AttributeType: S
        - AttributeName: pk
          AttributeType: S
        - AttributeName: sk
          AttributeType: S
      TableClass: STANDARD 
      KeySchema: 
        - AttributeName: pk
          KeyType: HASH
        - AttributeName: sk
          KeyType: RANGE
      ProvisionedThroughput: 
        ReadCapacityUnits: 5
        WriteCapacityUnits: 5
      BillingMode: PROVISIONED
      DeletionProtectionEnabled: !Ref DeletionProtectionEnabled
      GlobalSecondaryIndexes:
        - IndexName: message-group-sk-index
          KeySchema:
            - AttributeName: message_group_uuid
              KeyType: HASH
            - AttributeName: sk
              KeyType: RANGE
          Projection:
            ProjectionType: ALL
          ProvisionedThroughput: 
            ReadCapacityUnits: 5
            WriteCapacityUnits: 5
      StreamSpecification:
        StreamViewType: NEW_IMAGE
  ProcessDynamoDBStream:
    # https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: cruddur-messaging-stream
      PackageType: Zip
      Handler: lambda_handler
      Runtime: !Ref PythonRuntime
      Role: !GetAtt ExecutionRole.Arn
      MemorySize: !Ref MemorySize
      Timeout: !Ref Timeout
      Events:
        Stream:
          Type: DynamoDB
          Properties:
            Stream: !GetAtt DynamoDBTable.StreamArn
            # TODO - Does our Lambda handle more than record?
            BatchSize: 1
            # https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-dynamodb.html#sam-function-dynamodb-startingposition
            # TODO - This this the right value?
            StartingPosition: LATEST
  LambdaLogGroup:
    Type: "AWS::Logs::LogGroup"
    Properties:
      LogGroupName: "/aws/lambda/cruddur-messaging-stream00"
      RetentionInDays: 14
  LambdaLogStream:
    Type: "AWS::Logs::LogStream"
    Properties:
      LogGroupName: !Ref LambdaLogGroup
      LogStreamName: "LambdaExecution"
  ExecutionRole:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html
    Type: AWS::IAM::Role
    Properties:
      RoleName: CruddurDdbStreamExecRole
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: 'Allow'
            Principal:
              Service: 'lambda.amazonaws.com'
            Action: 'sts:AssumeRole'
      Policies:
        - PolicyName: "LambdaExecutionPolicy"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: "Allow"
                Action: "logs:CreateLogGroup"
                Resource: !Sub "arn:aws:logs:${AWS::Region}:${AWS::AccountId}:*"
              - Effect: "Allow"
                Action:
                  - "logs:CreateLogStream"
                  - "logs:PutLogEvents"
                Resource: !Sub "arn:aws:logs:${AWS::Region}:${AWS::AccountId}:log-group:${LambdaLogGroup}:*"
              - Effect: "Allow"
                Action:
                  - "ec2:CreateNetworkInterface"
                  - "ec2:DeleteNetworkInterface"
                  - "ec2:DescribeNetworkInterfaces"
                Resource: "*"
              - Effect: "Allow"
                Action:
                  - "lambda:InvokeFunction"
                Resource: "*"
              - Effect: "Allow"
                Action:
                  - "dynamodb:DescribeStream"
                  - "dynamodb:GetRecords"
                  - "dynamodb:GetShardIterator"
                  - "dynamodb:ListStreams"
                Resource: "*"
```

I added a file called ```build``` within ddb folder with the command below:

```sh
#! /usr/bin/env bash
set -e # stop the execution of the script if it fails

FUNC_DIR="/workspace/aws-bootcamp-cruddur-2023/ddb/cruddur-messaging-stream/"
TEMPLATE_PATH="/workspace/aws-bootcamp-cruddur-2023/ddb/template.yaml"
CONFIG_PATH="/workspace/aws-bootcamp-cruddur-2023/ddb/config.toml"

sam validate -t $TEMPLATE_PATH

echo "== build"
# https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-build.html
# --use-container
# use container is for building the lambda in a container
# it's still using the runtimes and its not a custom runtime
sam build \
--use-container \
--config-file $CONFIG_PATH \
--template $TEMPLATE_PATH \
--base-dir $FUNC_DIR
#--parameter-overrides
```

I added a file called ```package``` within ddb folder with the command below:

```sh
#! /usr/bin/env bash
set -e # stop the execution of the script if it fails

ARTIFACT_BUCKET="cfn-artifacts-afrolatino"
TEMPLATE_PATH="/workspace/aws-bootcamp-cruddur-2023/.aws-sam/build/template.yaml"
OUTPUT_TEMPLATE_PATH="/workspace/aws-bootcamp-cruddur-2023/.aws-sam/build/packaged.yaml"
CONFIG_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/ddb/config.toml"

echo "== package"
# https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-package.html
sam package \
  --s3-bucket $ARTIFACT_BUCKET \
  --config-file $CONFIG_PATH \
  --output-template-file $OUTPUT_TEMPLATE_PATH \
  --template-file $TEMPLATE_PATH \
  --s3-prefix "ddb"
```

I added a file called ```deploy``` within ddb folder with the command below:

```sh
#! /usr/bin/env bash
set -e # stop the execution of the script if it fails

PACKAGED_TEMPLATE_PATH="/workspace/aws-bootcamp-cruddur-2023/.aws-sam/build/packaged.yaml"
CONFIG_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/ddb/config.toml"

echo "== deploy"
# https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-deploy.html
sam deploy \
  --template-file $PACKAGED_TEMPLATE_PATH  \
  --config-file $CONFIG_PATH \
  --stack-name "CrdDdb" \
  --tags group=cruddur-ddb \
  --no-execute-changeset \
  --capabilities "CAPABILITY_NAMED_IAM"
```

Make the files created executable by running the commands below:

```sh
chmod u+x ./ddb/build
chmod u+x ./ddb/package
chmod u+x .ddb/deploy
```

Then run the following commands below to build and deploy the package :

```sh
./ddb/build
./ddb/package
./ddb/deploy
```

Move ```cruddur messaging stream.py``` to ```ddb``` folder


### CFN CICD <a name="paragraph7"></a>
	
As developers work on multiple clients or for a group that supports various AWS deployments,they may often find ourselves challenged with updating AWS CloudFormation. A CI/CD pipeline can be built to automate the process of updating CloudFormation. AWS CodePipeline can initiate a workflow that builds and tests a stack and then pushes it to production. The workflow can either create or manipulate an existing stack.

The diagram below illustrates the solution architecture of a fully functional CI/CD that updates the CloudFormation template. The pipeline starts automatically after applying the intended changes to the Bitbucket repository.


![CICDSummary](https://github.com/AfroLatino/aws-bootcamp-cruddur-2023/assets/78261965/e93d72ac-dfe5-4d6e-82d7-909e209f7d08)

**Reference**
	
[cloudthat](https://www.cloudthat.com/resources/blog/deploy-cicd-pipeline-aws-by-updating-cloudformation-template#:~:text=Introduction%20to%20CloudFormation,-As%20developers%20work&text=We%20can%20build%20a%20CI,or%20manipulate%20an%20existing%20stack)	
	
Create a s3 bucket called codepipeline-cruddur-artifacts-afrolatino using the command below:

- Navigate to AWS Management Console and serach for S3 in AWS Services
- Click on **Create bucket**
- Give **Bucket name** as **codepipeline-cruddur-artifacts-afrolatino**	(Bucket names are unique)
- Then click on **Create bucket**

Create cicd files within aws/cfn/cicd

#### Create Config Toml file <a name="subparagraph12"></a>

Create a folder called ```cicd``` within aws / cfn, then add a file called ```config.toml``` with the command below:

```sh
[deploy]
bucket = '$BUCKET_NAME'
region = '$AWS_DEFAULT_REGION'
stack_name = 'CrdCicd'

[parameters]
ServiceStack = 'CrdSrvBackendFlask'
ClusterStack = 'CrdCluster'
GitHubBranch = 'prod'
GithubRepo = 'aws-bootcamp-cruddur-2023'
ArtifactBucketName = "codepipeline-cruddur-artifacts-afrolatino"
```
	
#### Create Template file <a name="subparagraph13"></a>
	
Add a file within aws / cfn / cicd called ```template.yaml``` with the command below:

```sh
AWSTemplateFormatVersion: 2010-09-09
Description: |
  - CodeStar Connection V2 Github
  - CodePipeline
  - Codebuild
Parameters:
  GitHubBranch:
    Type: String
    Default: prod
  GithubRepo:
    Type: String
    Default: 'afrolatino/aws-bootcamp-cruddur-2023'
  ClusterStack:
    Type: String
  ServiceStack:
    Type: String
  ArtifactBucketName:
    Type: String
Resources:
  CodeBuildBakeImageStack:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: nested/codebuild.yaml
  CodeStarConnection:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html
    Type: AWS::CodeStarConnections::Connection
    Properties:
      ConnectionName: !Sub ${AWS::StackName}-connection
      ProviderType: GitHub
  Pipeline:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html
    Type: AWS::CodePipeline::Pipeline
    Properties:
      ArtifactStore:
        Location: !Ref ArtifactBucketName
        Type: S3
      RoleArn: !GetAtt CodePipelineRole.Arn
      Stages:
        - Name: Source
          Actions:
            - Name: ApplicationSource
              RunOrder: 1
              ActionTypeId:
                Category: Source
                Provider: CodeStarSourceConnection
                Owner: AWS
                Version: '1'
              OutputArtifacts:
                - Name: Source
              Configuration:
                ConnectionArn: !Ref CodeStarConnection
                FullRepositoryId: !Ref GithubRepo
                BranchName: !Ref GitHubBranch
                OutputArtifactFormat: "CODE_ZIP"
        - Name: Build
          Actions:
            - Name: BuildContainerImage
              RunOrder: 1
              ActionTypeId:
                Category: Build
                Owner: AWS
                Provider: CodeBuild
                Version: '1'
              InputArtifacts:
                - Name: Source
              OutputArtifacts:
                - Name: ImageDefinition
              Configuration:
                ProjectName: !GetAtt CodeBuildBakeImageStack.Outputs.CodeBuildProjectName
                BatchEnabled: false
        # https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference-ECS.html
        - Name: Deploy
          Actions:
            - Name: Deploy
              RunOrder: 1
              ActionTypeId:
                Category: Deploy
                Provider: ECS
                Owner: AWS
                Version: '1'
              InputArtifacts:
                - Name: ImageDefinition
              Configuration:
                # In Minutes
                DeploymentTimeout: "10"
                ClusterName:
                  Fn::ImportValue:
                    !Sub ${ClusterStack}ClusterName
                ServiceName:
                  Fn::ImportValue:
                    !Sub ${ServiceStack}ServiceName
  CodePipelineRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Statement:
        - Action: ['sts:AssumeRole']
          Effect: Allow
          Principal:
            Service: [codepipeline.amazonaws.com]
        Version: '2012-10-17'
      Path: /
      Policies:
        - PolicyName: !Sub ${AWS::StackName}EcsDeployPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Action:
                - ecs:DescribeServices
                - ecs:DescribeTaskDefinition
                - ecs:DescribeTasks
                - ecs:ListTasks
                - ecs:RegisterTaskDefinition
                - ecs:UpdateService
                Effect: Allow
                Resource: "*"
        - PolicyName: !Sub ${AWS::StackName}CodeStarPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Action:
                - codestar-connections:UseConnection
                Effect: Allow
                Resource:
                  !Ref CodeStarConnection
        - PolicyName: !Sub ${AWS::StackName}CodePipelinePolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Action:
                - s3:*
                - logs:CreateLogGroup
                - logs:CreateLogStream
                - logs:PutLogEvents
                - cloudformation:*
                - iam:PassRole
                - iam:CreateRole
                - iam:DetachRolePolicy
                - iam:DeleteRolePolicy
                - iam:PutRolePolicy
                - iam:DeleteRole
                - iam:AttachRolePolicy
                - iam:GetRole
                - iam:PassRole
                Effect: Allow
                Resource: '*'
        - PolicyName: !Sub ${AWS::StackName}CodePipelineBuildPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Action:
                - codebuild:StartBuild
                - codebuild:StopBuild
                - codebuild:RetryBuild
                Effect: Allow
                Resource: !Join
                  - ''
                  - - 'arn:aws:codebuild:'
                    - !Ref AWS::Region
                    - ':'
                    - !Ref AWS::AccountId
                    - ':project/'
                    - !GetAtt CodeBuildBakeImageStack.Outputs.CodeBuildProjectName
```

#### Create CodeBuild file <a name="subparagraph14"></a>
	
Create a folder called ```nested``` within aws / cfn / cicd, then add a file called ```codebuild.yaml``` with the command below:
	
```sh
AWSTemplateFormatVersion: 2010-09-09
Description: |
  Codebuild used for baking container images
  - Codebuild Project
  - Codebuild Project Role

Parameters:
  LogGroupPath:
    Type: String
    Description: "The log group path for CodeBuild"
    Default: "/cruddur/codebuild/bake-service"
  LogStreamName:
    Type: String
    Description: "The log group path for CodeBuild"
    Default: "backend-flask"
  CodeBuildImage:
    Type: String
    Default: aws/codebuild/amazonlinux2-x86_64-standard:4.0
  CodeBuildComputeType:
    Type: String
    Default: BUILD_GENERAL1_SMALL
  CodeBuildTimeoutMins:
    Type: Number
    Default: 5
  BuildSpec:
    Type: String
    Default: 'buildspec.yaml'
Resources:
  CodeBuild:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html
    Type: AWS::CodeBuild::Project
    Properties:
      QueuedTimeoutInMinutes: !Ref CodeBuildTimeoutMins
      ServiceRole: !GetAtt CodeBuildRole.Arn
      # PrivilegedMode is needed to build Docker images
      # even though we have No Artifacts, CodePipeline Demands both to be set as CODEPIPLINE
      Artifacts:
        Type: CODEPIPELINE
      Environment:
        ComputeType: !Ref CodeBuildComputeType
        Image: !Ref CodeBuildImage
        Type: LINUX_CONTAINER
        PrivilegedMode: true
      LogsConfig:
        CloudWatchLogs:
          GroupName: !Ref LogGroupPath
          Status: ENABLED
          StreamName: !Ref LogStreamName
      Source:
        Type: CODEPIPELINE
        BuildSpec: !Ref BuildSpec
  CodeBuildRole:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Statement:
        - Action: ['sts:AssumeRole']
          Effect: Allow
          Principal:
            Service: [codebuild.amazonaws.com]
        Version: '2012-10-17'
      Path: /
      Policies:
        - PolicyName: !Sub ${AWS::StackName}ECRPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Action:
                - ecr:BatchCheckLayerAvailability
                - ecr:CompleteLayerUpload
                - ecr:GetAuthorizationToken
                - ecr:InitiateLayerUpload
                - ecr:BatchGetImage
                - ecr:GetDownloadUrlForLayer
                - ecr:PutImage
                - ecr:UploadLayerPart
                Effect: Allow
                Resource: "*"
        - PolicyName: !Sub ${AWS::StackName}VPCPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Action:
                - ec2:CreateNetworkInterface
                - ec2:DescribeDhcpOptions
                - ec2:DescribeNetworkInterfaces
                - ec2:DeleteNetworkInterface
                - ec2:DescribeSubnets
                - ec2:DescribeSecurityGroups
                - ec2:DescribeVpcs
                Effect: Allow
                Resource: "*"
              - Action:
                - ec2:CreateNetworkInterfacePermission
                Effect: Allow
                Resource: "*"
        - PolicyName: !Sub ${AWS::StackName}Logs
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Action:
                - logs:CreateLogGroup
                - logs:CreateLogStream
                - logs:PutLogEvents
                Effect: Allow
                Resource:
                  - !Sub arn:aws:logs:${AWS::Region}:${AWS::AccountId}:log-group:${LogGroupPath}*
                  - !Sub arn:aws:logs:${AWS::Region}:${AWS::AccountId}:log-group:${LogGroupPath}:*
Outputs:
  CodeBuildProjectName:
    Description: "CodeBuildProjectName"
    Value: !Sub ${AWS::StackName}Project
```
	
### CFN Static Website Hosting Frontend <a name="paragraph8"></a>



## Stretch Homework Challenges

### Retrieving Load Balancer IPs via AWS CLI <a name="paragraph9"></a>

Run the following command to fetch the Load Balancer DNS name:

```sh
aws elbv2 describe-load-balancers --query LoadBalancers[*].DNSName
```

Please see the result below:

![LoadBalIPs](https://user-images.githubusercontent.com/78261965/236585086-26d50cc9-87da-4a34-87c0-be97374cdddc.png)


### Retrieving Relational Database Service (RDS) via AWS CLI <a name="paragraph10"></a>

Run the following command to fetch the RDS DNS name:

```sh
aws rds describe-db-instances --query=DBInstances[*].Endpoint.Address 
```

Please see the result below:

![RDSIPs](https://user-images.githubusercontent.com/78261965/236585756-21cc6292-921f-49a0-b449-90b9de58fc2a.png)

You can specify the particular region if you wish using the command below:

```sh
aws rds describe-db-instances --query=DBInstances[*].Endpoint.Address --region us-east-1
```

### Retrieving AWS Elastic Beanstalk Public IPs via AWS CLI <a name="paragraph11"></a>

Run the following command to fetch details of all the Elastic Beanstalk instances:

```sh
aws elasticbeanstalk describe-environments --query Environments[*].EndpointURL 
```

Please see the result below:

![ElasticIPs](https://user-images.githubusercontent.com/78261965/236586608-49147ae0-b4f6-4fb7-ad81-5afe3e2c2f4b.png)

You can specify the particular region if you wish using the command below:

```sh
aws elasticbeanstalk describe-environments --query Environments[*].EndpointURL --region us-east-1
```


## AWS CloudFormation Security Best Practices


### Table of contents
- [What is Infrastructure as Code](#introduction30)
- [AWS CloudFormation – Security Best Practices – AWS](#paragraph31)
- [AWS CloudFormation – Security Best Practices – Application](#paragraph32)


### What is Infrastructure as Code <a name="introduction30"></a>

What is Infrastructure as Code? Infrastructure is the server or work station where your application would be running. Infrastructure as Code is the ability to use code to create the same infrastructure of work servers automatically in a cloud context.


### AWS CloudFormation – Security Best Practices – AWS <a name="paragraph31"></a>

- Compliance standard is what your business requires from a Infrastructure as Code (IaC) service and is available in the region you need to operate in.
- Amazon Organizations SCP – to restrict actions like creation, deletion, modification of production CloudFormation Templates/Resources etc
- AWS CloudTrail is enabled & monitored to trigger alerts for malicious activities e.g. changes to Production environment etc.
- AWS Audit Manager, IAM Access Analyzer etc. 


### AWS CloudFormation – Security Best Practices – Application <a name="paragraph32"></a>

- Access Control – Roles or IAM Users for making changes in Amazon CloudFormation Template stacks or StackSets especially one for production.
- Security of the CloudFormation – Configuration access
- Security in the CloudFormation – Code Security Best Practices – SCA, SAST, Secret Scanner, DAST implemented in the CI/CD Pipeline
- Security of the CloudFormation entry points e.g. – private access points using AWS Private Link etc.
- Only use Trusted Source Control for sending changes to CloudFormation
- Develop process for continuously verifying if there is a change that may compromise the known state of a CI/CD pipeline.
	
