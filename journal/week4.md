# Week 4 — Postgres and RDS

## Required Homework 

### Connecting to PSQL via the client CLI tool

I was able to connect to PSQL via the clinet CLI tool using the command below:

```sh
psql -Upostgres --host localhost
```

### BIN Folder

I created anew folder called bin.

#### db-connect

This is used for establising connection to the database. 

To access the locsl database, use

```sh
.\bin\db-connect
```

**For Production**

```sh
.\bin\db-connect prod
```

```sh
if [ "$1" = "prod" ]; then
  echo "Running in production mode"
  URL=$PROD_CONNECTION_URL
else
  URL=$CONNECTION_URL
fi

psql $URL
```

I created a database called cruddur with the command below:

```sh
CREATE database cruddur;
```



Creating users

```sh
cruddur=> select * from users;
-[ RECORD 1 ]---+-------------------------------------
uuid            | 97aab7fc-54e4-4d24-b88a-e466a1fda5a1
display_name    | AfroLatino
handle          | AfroLatino
email           | xx@gmail.com
cognito_user_id | e8350cca-d6bf-4451-acdd-xxxxx
created_at      | 2023-03-14 04:35:49.565702
```


### Securing your Amazon RDS Postgres Database

Amazon RDS currently supports the following engines:

- Aurora (MySQL Compatible)

- Aurora (PostgreSQL Compatible)

- MariaDB

- MySQL

- Oracle

- PostgreSQL

- Microsoft SQL Server

![RDS Engines](https://user-images.githubusercontent.com/78261965/224863977-247ecf3e-4025-4d54-af87-5fb17f3ecb96.png)


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


