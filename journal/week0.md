# Week 0 — Billing and Architecture

## Bootcamp Overview

Margaret Valtierra, an AWS Community Hero, went over the business use case of our project.

Chris Williams, an AWS Community Hero, went through the Well-Architected tool on AWS Management Console. He also encouraged us to ask "dumb" questions if we were unsure of any requirements. Chris talked about how important Requirements, Risks, Constraints and Assumptions were to architecture.

Requirements must be verifiable, monitorable and feasible.

Risks could include user commitment and Late Delivery.

Some assumptions are; Budget is approved, Stakeholders will be available to make decisions and there will be sufficient network bandwidth.

Constraints could include time and budget.

He also categorised stakeholder expectation to project delivery to 3 categories; fast, cheap or good.

The architecture is usally divided into Conceptual Design, Logical Design and Physical Design. Lucid chart was used to create the logical design.

Andrew Brown asked if we could create a conceptual diagram on a napkin.


## Additional Youtube Videos

Andrew Brown created a youtube video on how to launch AWS CloudShell, Generate AWS credentials, Setting up AWS Budgets and Billing Alarms.

Chirag did a youtube video on Spend Considerations.

Ashish did one on Security Considerations.


### Homework Challenges

### I have set up MFA on my root account as advised by Ashish but only use my IAM account for tasks. This also have MFA set up.

IAM Roles are as follows:

https://us-east-1.console.aws.amazon.com/iamv2/home?region=us-east-1#/roles

IAM MFA set up is as follows:

https://us-east-1.console.aws.amazon.com/iamv2/home?region=us-east-1#/home

### Please see the link below of using EventBridge to hookup Health Dashboard to SNS and send notification when there is a service health issue.

https://us-east-1.console.aws.amazon.com/events/home?region=us-east-1#/rules


### Please find below a screenshot of my Architectural diagram of the CI/CD logical pipeline below:

![Cruddur Logical Architecture](https://user-images.githubusercontent.com/78261965/218863161-2d7bd51e-008e-47c3-bb36-d7be644c4285.png)

The link is as follows:

https://lucid.app/lucidchart/5dba407d-3c11-4eb6-83fb-877c530ebbf5/edit?invitationId=inv_a22c61ab-b1e5-4a07-a383-33508a66cb6a&page=0_0#

### I have opened a support ticket and requested a service limit as seen from the link below:

https://support.console.aws.amazon.com/support/home#/case/?displayId=11997932311&language=en

Case ID is 11997932311.

### I created a Billing Alarm as seen from the link below:

https://us-east-1.console.aws.amazon.com/sns/v3/home?region=us-east-1#/topics

### I created an AWS Budget as seen from the link below:

https://us-east-1.console.aws.amazon.com/billing/home?region=us-east-1#/budgets/overview

### I installed AWS CLI as seen from the link below:

https://github.com/AfroLatino/aws-bootcamp-cruddur-2023

### Please see a screenshot of my napkin design below:

![Cruddur Conceptual Napkin Design](https://user-images.githubusercontent.com/78261965/218870057-bed4e86d-aeb4-4508-83cf-735769da9112.jpg)

### My review of all the questions of each pillars in the Well Architected Tool are as follows:

There are 58 main questions on the AWS Well-Architected Tool comprised of 6 pillars.

## Operational Excellence Pillar

The Operational Excellence pillar includes the ability to support development and run workloads effectively, gain insight into your operations, and to continuously improve supporting processes and procedures to deliver business value. 

## Design Principles:

-	Perform operations as code
-	Make frequent, small, reversible changes
-	Refine operations procedures frequently
-	Anticipate failure
-	Learn from all operational failures

## Best Practices Topics and Considerations:

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

## Self-Assessment Questions:

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

## Level of Risk exposed if these best practices are not established:

-	There are 82 sub-questions; 34 with High Risk, 31 with Medium risk and 17 with Low Risk. 

## Security Pillar

The security pillar describes how to take advantage of cloud technologies to protect data, systems, and assets in a way that can improve your security posture.

## Design Principles:

-	Implement a strong identity foundation
-	Enable traceability
-	Apply security at all layers
-	Automate security best practices
-	Protect data in transit and at rest
-	Keep people away from data
-	Prepare for security events

## Best Practices Topics and Considerations:

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

## Self-Assessment Questions:

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

## Level of Risks exposed if these best practices are not established:

-	There are 56 sub-questions; 25 with High Risk, 16 with Medium risk and 15 with Low Risk. 

## Reliability Pillar

The Reliability pillar encompasses the ability of a workload to perform its intended function correctly and consistently when it’s expected to. 

## Design Principles:

-	Automatically recover from failure
-	Test recovery procedures
-	Scale horizontally to increase aggregate workload availability
-	Stop guessing capacity
-	Manage change in automation

## Best Practices Topics and Considerations:

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

## Self-Assessment Questions:

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

## Level of Risks exposed if these best practices are not established:

- There are 66 sub-questions; 34 with High Risk, 30 with Medium risk and 2 with Low Risk. 

## Performance Efficiency Pillar

The Performance Efficiency pillar includes the ability to use computing resources efficiently to meet system requirements, and to maintain that efficiency as demand changes and technologies evolve. 

## Design Principles:

-	Democratize advanced technologies
-	Go global in minutes
-	Use serverless architectures
-	Experiment more often
-	Consider mechanical sympathy

## Best Practices Topics and Considerations:

-	Selection -> Performance Architecture Selection
-	Selection -> Compute Architecture Selection
-	Selection -> Storage Architecture Selection
-	Selection -> Database Architecture Selection
-	Selection -> Networking Configuration Solution
-	Review -> Evolving Workload to Take Advantage of New Releases
-	Monitoring -> Monitoring Resources 
-	Trade-offs -> Using Trade-offs to Improve Performance

## Self-Assessment Questions:

-	PERF 1: How do you select the best performing architecture?
-	PERF 2: How do you select your compute solution?
-	PERF 3: How do you select your storage solution?
-	PERF 4: How do you select your database solution?
-	PERF 5: How do you configure your networking solution?
-	PERF 6: How do you evolve your workload to take advantage of new releases?
-	PERF 7:  How do you monitor your resources to ensure they are performing?
-	PERF 8: How do you use trade-offs to improve performance?

## Level of Risks exposed if these best practices are not established:

-	There are 42 sub-questions; 20 with High Risk, 14 with Medium risk and 8 with Low Risk. 

## Cost Optimization Pillar

The Cost Optimization pillar includes the ability to run systems to deliver business value at the lowest price point.

## Design Principles:

-	Implement Cloud Financial Management
-	Adopt a consumption model
-	Measure overall efficiency
-	Stop spending money on undifferentiated heavy lifting
-	Analyze and attribute expenditure

## Best Practices Topics and Considerations:

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

## Self-Assessment Questions:

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

## Level of Risks exposed if these best practices are not established:

-	There are 47 sub-questions; 19 with High Risk, 5 with Medium risk and 23 with Low Risk. 

## Sustainability Pillar

The Sustainability pillar focuses on environmental impacts, especially energy consumption and efficiency, since they are important levers for architects to inform direct action to reduce resource usage. 

## Design Principles:

-	Understand your impact
-	Establish sustainability goals
-	Maximize utilization
-	Anticipate and adopt new, more efficient hardware and software offerings
-	Use managed services
-	Reduce the downstream impact of your cloud workloads

## Best Practices Topics and Considerations:

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

## Self-Assessment Questions:

-	SUS 1: How do you select Regions to support your sustainability goals?
-	SUS 2: How do you take advantage of user behavior patterns to support your sustainability goals?
-	SUS 3: How do you take advantage of software and architecture patterns to support your sustainability goals?
-	SUS 4: How do you take advantage of data access and usage patterns to support your sustainability goals?
-	SUS 5: How do your hardware management and usage practices support your sustainability goals?
-	SUS 6: How do your development and deployment processes support your sustainability goals?

## Level of Risks exposed if these best practices are not established:

-	There are 27 sub-questions; 6 with Medium risk and 21 with Low Risk. 


### Challenges faced whilst doing the homework

- I made a mistake whilst trying to install CLI on Gitpod. I didn't amend one of the files copied as a json file, so got an error message. I later realised this and fixed it.
- I faced difficulty trying to import the moment icon into Lucid charts but I was finally able to do this.
- It took me longer to complete most of the tasks as this was my first time doing them. However, your videos were very helpful. Thank you very much!

