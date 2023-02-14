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

