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

## Operational Excellence Pillar

The Operational Excellence pillar includes the ability to support development and run workloads effectively, gain insight into your operations, and to continuously improve supporting processes and procedures to deliver business value. 

## Design Principles:

-	Perform operations as code
-	Make frequent, small, reversible changes
-	Refine operations procedures frequently
-	Anticipate failure
-	Learn from all operational failures

## Best Practices Topics and Categories:

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

# Design Principles:
-	Implement a strong identity foundation
•	Enable traceability
•	Apply security at all layers
•	Automate security best practices
•	Protect data in transit and at rest
•	Keep people away from data
•	Prepare for security events

Best Practices Topics and Categories:
•	Security > Operation of Workloads Securely

•	Identity & Access Management -> Identity Management for people and machines
•	Identity & Access Management -> Permissions Management for people and machines
•	Detection -> Investigation of Security Events
•	Infrastructure Protection -> Protecting Network Resources
•	Infrastructure Protection ->Protecting Computer Resources
•	Data Protection > Data Classification
•	Data Protection > Data Protection at Rest
•	Data Protection > Data Protection in Transit
•	Incident Response > Anticipation, Response and Recovery from Incidents

Self-Assessment Questions:
•	SEC 1: How do you securely operate your workload?
•	SEC 2: How do you manage authentication for people and machines?
•	SEC 3: How do you manage permissions for people and machines?
•	SEC 4: How do you detect and investigate security events?
•	SEC 5: How do you protect your network resources?
•	SEC 6: How do you protect your compute resources?
•	SEC 7: How do you classify your data?
•	SEC 8: How do you protect your data at rest?
•	SEC 9: How do you protect your data in transit?
•	SEC 10: How do you anticipate, respond to, and recover from incidents?
Level of Risk exposed if this best practice is not established:
•	There are 56 sub-questions; 25 with High Risk, 16 with Medium risk and 15 with Low Risk. 



