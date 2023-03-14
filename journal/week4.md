# Week 4 — Postgres and RDS

## Required Homework 

### Amazon RDS – Security Best Practices – AWS

-	Use VPCs: Use Amazon Virtual Private Cloud (VPC) to create a private network for your RDS instance. This helps prevent unauthorised access to your instance from the public internet.
-	Compliance standard is what your business requires.
-	RDS instances should only be in the AWS Region that you are legally allowed to be holding user data in.
-	Amazon Organisations SCP – to manage RDS deletion, RDS creation, region lock, RDS Encryption enforced etc.
-	AWS CloudTrail is enabled and monitored to trigger alerts on malicious RDS behaviour by an identity in RWS.
-	Amazon Guardduty is enabled in the account and region of RDS.

### Amazon RDS – Security Best Practices – Application

-	RDS Instance to use appropriate authentication – Use IAM authentication, Kerberos etc (not the default).
- Database User Lifecycle Management – Create, Modify, Delete Users.
-	AWS User Access Lifecycle Management – Change of Roles/Revoke Roles etc.
-	Security Group to be restricted only to known IPs.
-	Not have RDS be internet (publicly) accessible.
-	Encryption in Transit for comms between App & RDS
-	Secret Management: Master User passwords can be used with AWS Secrets Manager to automatically rotate the secrets for Amazon RDS.

