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


## Stretch Homework Challenges

## Table of contents

- [Retrieving Load Balancer IPs via AWS CLI](#paragraph6)
- [Retrieving Relational Database Service (RDS) IPs via AWS CLI](#paragraph7)
- [Retrieving AWS Elastic Beanstalk Public IPs via AWS CLI](#paragraph8)


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

![CFNdiagramming](https://user-images.githubusercontent.com/78261965/236579058-19079df7-665e-4feb-b611-3bcebf92f159.png)


[Lucid Sharelink](https://lucid.app/lucidchart/da017170-fa3e-40c1-bcc9-6ee836005ddc/edit?viewport_loc=-1944%2C-865%2C3657%2C1646%2C0_0&invitationId=inv_690a7f45-a65b-4bd4-b161-266dbc273a6e)


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




## Stretch Homework Challenges


### Retrieving Load Balancer IPs via AWS CLI <a name="paragraph6"></a>

Run the following command to fetch the Load Balancer DNS name:

```sh
aws elbv2 describe-load-balancers --query LoadBalancers[*].DNSName
```

Please see the result below:

![LoadBalIPs](https://user-images.githubusercontent.com/78261965/236585086-26d50cc9-87da-4a34-87c0-be97374cdddc.png)


### Retrieving Relational Database Service (RDS) via AWS CLI <a name="paragraph7"></a>

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

### Retrieving AWS Elastic Beanstalk Public IPs via AWS CLI <a name="paragraph8"></a>

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
	
