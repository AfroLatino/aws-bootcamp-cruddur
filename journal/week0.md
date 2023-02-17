# Week 0 — Billing and Architecture

## Required Homework Challenges

### Destroy your root account credentials

I do not have any access keys attached to my root account. I have also set up MFA as advised by Ashish on his security video.


### MFA Set-up on Root and IAM user accounts

![MFA Set-up](https://user-images.githubusercontent.com/78261965/219657999-1c4b4779-f2fb-4c12-b2bc-d67c27e2a649.png)

[MFA Set-up Share Link](https://us-east-1.console.aws.amazon.com/iamv2/home?region=us-east-1#/home)


### IAM Role

My IAM Role is called IAMRole. The screenshot and share link are as follows:

![IAM Role](https://user-images.githubusercontent.com/78261965/219116905-7d7b4c8f-bb66-400d-b3df-9ee0aeeb0954.png)

[IAM Role Share Link](https://us-east-1.console.aws.amazon.com/iamv2/home?region=us-east-1#/roles)


### Amazon EventBridge to hookup Health Dashboard to SNS and send notification when there is a service health issue.

The screenshot and share link of my Amazon EventBridge called Health Dashboard are as follows:

![Amazon EventBridge](https://user-images.githubusercontent.com/78261965/219118679-9fb9b1cb-de05-463d-a375-6a48c502de43.png)

[Amazon EventBridge Share Link](https://us-east-1.console.aws.amazon.com/events/home?region=us-east-1#/rules)


### My review of all the questions of each pillars in the Well Architected Tool are as follows:

There are 58 main questions on the AWS Well-Architected Tool comprised of 6 pillars.

### Operational Excellence Pillar

The Operational Excellence pillar includes the ability to support development and run workloads effectively, gain insight into your operations, and to continuously improve supporting processes and procedures to deliver business value. 

#### Design Principles:

-	Perform operations as code
-	Make frequent, small, reversible changes
-	Refine operations procedures frequently
-	Anticipate failure
-	Learn from all operational failures

#### Best Practices Topics and Considerations:

-	Organization -> Organizational Priorities
-	Organization -> Organizational Structure
-	Organization -> Organizational Culture
-	Prepare -> Design Workload
-	Prepare -> Design for Operations
-	Prepare -> Mitigate Deployment Risks
-	Prepare -> Operational Readiness 
-	Operate -> Understanding Workload Health
-	Operate -> Understanding Operational Health
-	Operate -> Managing Workload and Operational Events
-	Evolve -> Evolving Operations

#### Self-Assessment Questions:

-	OPS 1:  How do you determine what your priorities are?
-	OPS 2:  How do you structure your organization to support your business outcomes?
-	OPS 3:  How does your organizational culture support your business outcomes?
-	OPS 4:  How do you design your workload so that you can understand its state?
-	OPS 5:  How do you reduce defects, ease remediation, and improve flow into production?
-	OPS 6:  How do you mitigate deployment risks?
-	OPS 7:  How do you know that you are ready to support a workload?
-	OPS 8:  How do you understand the health of your workload?
-	OPS 9:  How do you understand the health of your operations?
-	OPS 10: How do you manage workload and operations events?
-	OPS 11: How do you evolve operations?

#### Level of Risk exposed if these best practices are not established:

-	There are 82 sub-questions; *34* with *High Risk*, *31* with *Medium risk* and *17* with *Low Risk*. 

### Security Pillar

The security pillar describes how to take advantage of cloud technologies to protect data, systems, and assets in a way that can improve your security posture.

#### Design Principles:

-	Implement a strong identity foundation
-	Enable traceability
-	Apply security at all layers
-	Automate security best practices
-	Protect data in transit and at rest
-	Keep people away from data
-	Prepare for security events

#### Best Practices Topics and Considerations:

-	Security -> Operation of Workloads Securely
-	Identity & Access Management -> Identity Management for people and machines
-	Identity & Access Management -> Permissions Management for people and machines
-	Detection -> Investigation of Security Events
-	Infrastructure Protection -> Protecting Network Resources
-	Infrastructure Protection -> Protecting Computer Resources
-	Data Protection -> Data Classification
-	Data Protection -> Data Protection at Rest
-	Data Protection -> Data Protection in Transit
-	Incident Response -> Anticipation, Response and Recovery from Incidents

#### Self-Assessment Questions:

-	SEC 1: How do you securely operate your workload?
-	SEC 2: How do you manage authentication for people and machines?
-	SEC 3: How do you manage permissions for people and machines?
-	SEC 4: How do you detect and investigate security events?
-	SEC 5: How do you protect your network resources?
-	SEC 6: How do you protect your compute resources?
-	SEC 7: How do you classify your data?
-	SEC 8: How do you protect your data at rest?
-	SEC 9: How do you protect your data in transit?
-	SEC 10: How do you anticipate, respond to, and recover from incidents?

#### Level of Risks exposed if these best practices are not established:

-	There are 56 sub-questions; *25* with *High Risk*, *16* with *Medium risk* and *15* with *Low Risk*. 

### Reliability Pillar

The Reliability pillar encompasses the ability of a workload to perform its intended function correctly and consistently when it’s expected to. 

#### Design Principles:

-	Automatically recover from failure
-	Test recovery procedures
-	Scale horizontally to increase aggregate workload availability
-	Stop guessing capacity
-	Manage change in automation

#### Best Practices Topics and Considerations:

-	Foundations -> Manage Service Quotas and Constraints
-	Foundations -> Plan your Network Topology
-	Workload Architecture -> Design Your Workload Service Architecture
-	Workload Architecture -> Design Interactions in a Distributed System to Prevent Failures
-	Workload Architecture -> Design Interactions in a Distributed System to Mitigate or Withstand Failures
-	Change Management -> Monitor Workload Resources
-	Change Management -> Design your Workload to Adapt to Changes in Demand
-	Change Management -> Implement Change
-	Failure Management -> Back up Data
-	Failure Management -> Use Fault Isolation to Protect Your Workload
-	Failure Management -> Design your Workload to Withstand Component Failures
-	Failure Management -> Test Reliability
-	Failure Management -> Plan for Disaster Recovery (DR)

#### Self-Assessment Questions:

-	REL 1: How do you manage service quotas and constraints?
-	REL 2: How do you plan your network topology?
-	REL 3: How do you design your workload service architecture?
-	REL 4: How do you design interactions in a distributed system to prevent failures?
-	REL 5: How do you design interactions in a distributed system to mitigate or withstand failures?
-	REL 6: How do you monitor workload resources?
-	REL 7: How do you design your workload to adapt to changes in demand?
-	REL 8: How do you implement change?
-	REL 9: How do you back up data?
-	REL 10: How do you use fault isolation to protect your workload?
-	REL 11: How do you design your workload to withstand component failures?
-	REL 12: How do you test reliability?
-	REL 13: How do you plan for disaster recovery (DR)?

#### Level of Risks exposed if these best practices are not established:

- There are 66 sub-questions; *34* with *High Risk*, *30* with *Medium risk* and *2* with *Low Risk*. 

### Performance Efficiency Pillar

The Performance Efficiency pillar includes the ability to use computing resources efficiently to meet system requirements, and to maintain that efficiency as demand changes and technologies evolve. 

#### Design Principles:

-	Democratize advanced technologies
-	Go global in minutes
-	Use serverless architectures
-	Experiment more often
-	Consider mechanical sympathy

#### Best Practices Topics and Considerations:

-	Selection -> Performance Architecture Selection
-	Selection -> Compute Architecture Selection
-	Selection -> Storage Architecture Selection
-	Selection -> Database Architecture Selection
-	Selection -> Networking Configuration Solution
-	Review -> Evolving Workload to Take Advantage of New Releases
-	Monitoring -> Monitoring Resources 
-	Trade-offs -> Using Trade-offs to Improve Performance

#### Self-Assessment Questions:

-	PERF 1: How do you select the best performing architecture?
-	PERF 2: How do you select your compute solution?
-	PERF 3: How do you select your storage solution?
-	PERF 4: How do you select your database solution?
-	PERF 5: How do you configure your networking solution?
-	PERF 6: How do you evolve your workload to take advantage of new releases?
-	PERF 7:  How do you monitor your resources to ensure they are performing?
-	PERF 8: How do you use trade-offs to improve performance?

#### Level of Risks exposed if these best practices are not established:

-	There are 42 sub-questions; *20* with *High Risk*, *14* with *Medium risk* and *8* with *Low Risk*. 

#### Cost Optimization Pillar

The Cost Optimization pillar includes the ability to run systems to deliver business value at the lowest price point.

#### Design Principles:

-	Implement Cloud Financial Management
-	Adopt a consumption model
-	Measure overall efficiency
-	Stop spending money on undifferentiated heavy lifting
-	Analyze and attribute expenditure

#### Best Practices Topics and Considerations:

-	Practice Cloud Financial Management -> Implementing Cloud Financial Management 
-	Expenditure and usage awareness -> Usage Governance
-	Expenditure and usage awareness -> Monitor Cost and Usage
-	Expenditure and usage awareness -> Decommission Resources
-	Cost-effective resources -> Evaluating Cost When Selecting Services
-	Cost-effective resources -> Meeting Cost Targets
-	Cost-effective resources -> Select the Best Pricing Model
-	Cost-effective resources -> Plan for Data Transfer Charges
-	Manage demand and supply resources -> Manage Demand
-	Optimize over time -> Evaluation of New Services

#### Self-Assessment Questions:

-	COST 1: How do you implement cloud financial management?
-	COST 2: How do you govern usage?
-	COST 3: How do you monitor usage and cost?
-	COST 4: How do you decommission resources?
-	COST 5: How do you evaluate cost when you select services?
-	COST 6: How do you meet cost targets when you select resource type, size and number?
-	COST 7: How do you use pricing models to reduce cost?
-	COST 8: How do you plan for data transfer charges?
-	COST 9: How do you manage demand, and supply resources?
-	COST 10: How do you evaluate new services?

#### Level of Risks exposed if these best practices are not established:

-	There are 47 sub-questions; *19* with *High Risk*, *5* with *Medium risk* and *23* with *Low Risk*. 

### Sustainability Pillar

The Sustainability pillar focuses on environmental impacts, especially energy consumption and efficiency, since they are important levers for architects to inform direct action to reduce resource usage. 

#### Design Principles:

-	Understand your impact
-	Establish sustainability goals
-	Maximize utilization
-	Anticipate and adopt new, more efficient hardware and software offerings
-	Use managed services
-	Reduce the downstream impact of your cloud workloads

#### Best Practices Topics and Considerations:

-	Region selection -> Choose Regions near Amazon renewable energy projects  
-	User behavior patterns -> Scale infrastructure with user load
-	User behavior patterns -> Align SLAs with sustainability goals
-	User behavior patterns -> Eliminate creation and maintenance of unused assets
-	User behavior patterns -> Optimize geographic placement of workloads for user locations
-	User behavior patterns -> Optimize team member resources for activities performed
-	Software and architecture patterns -> Optimize software and architecture for asynchronous and scheduled jobs
-	Software and architecture patterns -> Remove or refactor workload components with low or no use 
-	Software and architecture patterns -> Optimize areas of code that consume the most time or resources
-	Software and architecture patterns -> Optimize impact on customer devices and equipment
-	Data patterns -> Implement a data classification policy
-	Data patterns -> Use technologies that support data access and storage patterns
-	Data patterns -> Use lifecycle policies to delete unnecessary data
-	Data patterns -> Minimize over-provisioning in block storage
-	Data patterns -> Remove unneeded or redundant data
-	Data patterns -> Use shared file systems or object storage to access common data
-	Data patterns -> Back up data only when difficult to recreate
-	Hardware patterns -> Use the minimum amount of hardware to meet your needs
-	Hardware patterns -> Use instance types with the least impact
-	Hardware patterns -> Use managed services
-	Hardware patterns -> Optimize your use of GPUs
-	Development and deployment process > Adopt methods that can rapidly introduce sustainability improvements
-	Development and deployment process > Keep your workload up to date
-	Development and deployment process > Increase utilization of build environments
-	Development and deployment process > Use managed device farms for testing

#### Self-Assessment Questions:

-	SUS 1: How do you select Regions to support your sustainability goals?
-	SUS 2: How do you take advantage of user behavior patterns to support your sustainability goals?
-	SUS 3: How do you take advantage of software and architecture patterns to support your sustainability goals?
-	SUS 4: How do you take advantage of data access and usage patterns to support your sustainability goals?
-	SUS 5: How do your hardware management and usage practices support your sustainability goals?
-	SUS 6: How do your development and deployment processes support your sustainability goals?

#### Level of Risks exposed if these best practices are not established:

-	There are 27 sub-questions; *6* with *Medium risk* and *21* with *Low Risk*. 

### References

References are as follows:

[Hyperglance Share Link](https://www.hyperglance.com/blog/aws-well-architected/)

[AWS Well Architected Share Link](https://docs.aws.amazon.com/wellarchitected/latest/framework/oe-prepare.html)


### Architectural diagram of AWS CI/CD logical pipeline using Kubernetes:

Please find below a screenshot of my architectural diagram of AWS CI/CD logical pipeline using Kubernetes.

![AWS CI_CD pipeline using Kubernetes](https://user-images.githubusercontent.com/78261965/218963681-8363ddd5-2dde-4c7e-9bb8-ef14fd030920.png)

The link is as follows:

[AWS CI_CD pipeline using Kubernetes Share link](https://lucid.app/lucidchart/defe270e-cc64-4e1d-8655-f23a35e07d1e/edit?viewport_loc=-11%2C55%2C1699%2C690%2C0_0&invitationId=inv_785e5048-e221-47e6-ad0b-4716e3abe4d6)


### The technical and service limits of specific services and how they could impact the technical path for technical flexibility

### Amazon S3

Amazon Simple Storage Service (Amazon S3) is an object storage service offering industry-leading scalability, data availability, security, and performance. Customers of all sizes and industries can store and protect any amount of data for virtually any use case, such as data lakes, cloud-native applications, and mobile apps. With cost-effective storage classes and easy-to-use management features, you can optimize costs, organize data, and configure fine-tuned access controls to meet specific business, organizational, and compliance requirements.

5 GB of S3 standard storage is available for 12 months with AWS Free Tier.

AWS charges less where their costs are less. For example, their costs are lower in the US East (Northern Virginia) Region than in the US West (Northern California) Region.

For example, the S3 Standard - General purpose storage for any type of data, typically used for frequently accessed data, for the first 50 TB per month for Europe (Paris) Region is $0.024 per GB. The next 450 TB per month is $0.023 per GB and $0.022 per GB over 500TB.

For South America (Sao Paulo) region, this is $0.0405 per GB. The next 450 TB per month is $0.039 per GB and $0.037 per GB over 500TB. This shows that those using the Sao Paulo region would have to pay more for these services. For those that can not afford these rates and would only want to use Sao Paulo region for several factors, they may decide not to store their frequently accessed data effectively, thereby negatively impacting their technical path and flexibility.

The advantage is that Amazon S3 is available in AWS Regions worldwide, and one can use Amazon S3 regardless of their location. This then have a positive impact on a user’s technical path and flexibility. 

There are no additional charges for using Amazon S3 for event notifications. One pays only for use of Amazon SNS or Amazon SQS to deliver event notifications. In situations where Amazon SNS or Amazon SQS may be the better option to deliver event notifications, users may not opt for either of these because of financial constraints. This would, in return, prevent users from learning how to use these services, thereby affecting their technical path and may also negatively affect service delivery if event notifications are not utilised.

When you create a bucket, you choose its name and the AWS Region to create it in. After you create a bucket, you can't change its name or Region. There may be users that had to create a bucket based on the existing regions or customer base at the time of creation. These users will be unable to change their Regions to take advantage of lower rates or being closer to their new customer base in the future. There are also instances where companies may want to rename their companies and amend all previous names. If the bucket was linked to the previous company name, they will be unable to change this.

### AWS Free Tier

Your AWS usage stays within the AWS Free Tier limits when all of these conditions are met:

•	You’re within the first 12 months of creating your AWS account.
•	You use only AWS services that offer AWS Free Tier benefits.
•	Your usage stays within the AWS Free Tier limits of those services.

If you use AWS services beyond one or more of these conditions, then that usage exceeds the Free Tier limits. You're charged at the standard AWS billing rates for usage that exceeds the Free Tier limits.

During the Free Tier period, about 36 services or more offer you free usage up to certain limits.

This only applies to some kinds of usage even within those limits. E.g. for EC2, you get 750 hours a month of t2 or t3 micro instance usage. If you spin up a c5.small instance instead, you will be billed starting as soon as you hit the launch button. 

You get a free t2.micro in regions where they are available. In regions where they are not, you instead get a free t3.micro. Get this wrong in either direction and you are paying for it.

You get 1GB of data transfer out to the internet for free each month in perpetuity. However, you will get charged for data transfer to other availability zones in the same AWS region. Further, that free 1GB is shared between a whole bunch of services; you can use it up quickly if you are not careful.

In Free Tier services, one can get a free load balancer but it is only an ELB Classic or an Application Load Balancer. If you pick a Network Load Balancer or NLB, it costs you money. You can get a free Oracle RDS instance but only if you bring your own license.

AWS Free Tier version is a service specific limited-time trial period that begins from your first use of a service. This applies to any use of the service, by any user in the account.

If one of your users spins up an Amazon Workspace to test something one day then turns it off, that free trial is over for the entire AWS account once the trial period ends. If you enable Amazon Detective, it will be free for 30 days, so your next bill is care-free and breezy. However, there may be some charges to your next bill.

A new user may not know any of the conditions above and utilise some of the services that incur charges thinking they are on a free tier service. Hence, they will be charged which results in them closing their account in panic. This would consequently affect their training and development and have a negative impact on their technical path.

### CloudWatch 

The Alarm Actions resource has a default quota of 5 per alarm. This quota cannot be changed. Hence, users that may need more than 5 won’t be able to have this functionality. 

For Metrics Insights queries resource, a single query can process no more than 10,000 metrics. This means that if the SELECT, FROM, and WHERE clauses would match more than 10,000 metrics, only the first 10,000 of these metrics that are found will be processed by the query.

A single query can return no more than 500 time series.

You can query only the most recent three hours of data.

These are limitations for users that may want to process more than 10,000 metrics or return 600 time series or query the most recent 24 hours of data. These would in effect negatively affect the technical path for technical flexibility.

### AWS Control Tower

There are known limitations and unsupported use cases in AWS Control Tower.

-	AWS Control Tower has overall concurrency limitations. In general, one operation at a time is permitted. Two exceptions to this limitation are allowed:
    -	Optional controls can be activated and deactivated concurrently, through an asynchronous process. Up to ten (10) control-related operations at a time can be in progress
    - Accounts can be provisioned, updated, and enrolled concurrently in Account Factory, through an asynchronous process, with up to five (5) account-related operations in progress simultaneously.
-	Email addresses of shared accounts in the Security OU can be changed, but you must update your landing zone to see these changes in the AWS Control Tower console.
-	A limit of 5 SCPs per OU applies to OUs in your AWS Control Tower landing zone.
-	Existing OUs with over 300 accounts cannot be registered or re-registered in AWS Control Tower.
-	The limit for EnableControl and DisableControl updates in AWS Control Tower is 10 concurrent operations.

You can contact AWS Support to request a limit increase for some resources in AWS Control Tower. For example, you can request a limit increase from five of up to ten (10) concurrent account-related operations. Some AWS Control Tower performance metrics may change after a limit increase.
When provisioning new accounts in this environment, you can use lifecycle events to trigger automated requests for service limit increases in specified AWS Regions.

#### Control limitations

If you modify AWS Control Tower resources, such as an SCP, or remove any AWS Config resource, such as a Config recorder or aggregator, AWS Control Tower can no longer guarantee that the controls are functioning as designed. Therefore, the security of your multi-account environment may be compromised. The AWS shared responsibility model of security is applicable to any such changes you may make.

AWS Control Tower helps maintain the integrity of your environment by resetting the SCPs of the controls to their standard configuration when you update your landing zone. Changes that you may have made to SCPs are replaced by the standard version of the control, by design.

## References

References are as follows; 

[Control Tower Share Link](https://docs.aws.amazon.com/controltower/latest/userguide/limits.html)

[Amazon S3 Share Link](https://aws.amazon.com/s3/)

[Amazon Free Tire Share Link](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=*all)

[AWS Service Limits Share Link](https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html)


### Opening a support ticket and requesting a service limit

Please find the screen shot of the support ticket requesting a service limit below:

![Service Limit Support Ticket](https://user-images.githubusercontent.com/78261965/219122623-a7ae65d8-d516-477b-a0f7-2229c002f5a1.png)

Case ID is 11997932311.

The share link is as follows:

[Service Limit Support Ticket Share Link](https://support.console.aws.amazon.com/support/home#/case/?displayId=11997932311&language=en)


### Challenges faced whilst doing the homework

- I made a mistake whilst trying to install CLI on Gitpod. I didn't amend one of the files copied as a json file, so got an error message. I later realised this and fixed it.
- I faced difficulty trying to import the momento.svg icon into Lucid charts but I was finally able to do this.
- It took me a fair bit of time to complete most of the tasks as I am very new to this field. However, your videos were very helpful. Thank you very much!


## Additional Homework Challenges

### Billing Alarm 

I created 2 billing alarms; one was created for the SNS notification when there is a service health issue for the homework challenge.

The screenshot and share link are as follows:

![AWS Billing Alarms](https://user-images.githubusercontent.com/78261965/219127583-59507b1d-aaf6-46f5-867d-fa6a37d16dfc.png)

[AWS Billing Alarms Share Link](https://us-east-1.console.aws.amazon.com/sns/v3/home?region=us-east-1#/topics)


### AWS Budget 

I created 2 AWS Budgets with a spend of $1.00 for demo purposes.

The screenshot and share link are as follows:

![AWS Budgets](https://user-images.githubusercontent.com/78261965/219128647-81c46c29-5f41-43a5-ae61-6ca996c9be9e.png)

[AWS Budget Share Link](https://us-east-1.console.aws.amazon.com/billing/home?region=us-east-1#/budgets/overview)


### AWS CLI 

I installed AWS CLI as seen from the link below:

[AWS CLI Share Link](https://github.com/AfroLatino/aws-bootcamp-cruddur-2023)


### Napkin Design

Please find below a screenshot of my Cruddur Conceptual Napkin Design

![Cruddur Conceptual Napkin Design](https://user-images.githubusercontent.com/78261965/218870057-bed4e86d-aeb4-4508-83cf-735769da9112.jpg)


### Recreation of Conceptual Architectural Diagram

I also re-created the conceptual architectural diagram in LucidCharts by Andrew Brown.

The screenshot and share link are as follows:

![Cruddur Logical Architecture](https://user-images.githubusercontent.com/78261965/219129942-f4f81465-05f5-490b-a7b9-efb7d6d2f1a8.png)

[Recreation of Conceptual Architectural Diagram By Andrew Brown](https://lucid.app/lucidchart/5dba407d-3c11-4eb6-83fb-877c530ebbf5/edit?viewport_loc=-301%2C207%2C2550%2C1152%2C0_0&invitationId=inv_a22c61ab-b1e5-4a07-a383-33508a66cb6a)



