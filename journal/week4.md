# Week 4 — Postgres and RDS

## Required Homework 

### Connecting to PSQL via the client CLI tool

I was able to connect to PSQL via the clinet CLI tool using the command below:

```sh
psql -Upostgres --host localhost
```

### Setting up RDS Instance

A RDS database called cruddur-db-instance was set up using PostgreSQL engine.

![cruddur instance](https://user-images.githubusercontent.com/78261965/226113423-1e1165c1-43b9-4c1b-af34-f8e2d4a8e8aa.png)

The Security Groups and VPC were set with backups disabled.

The database can be stopped temporarily if not in use. Please note that this automatically starts back up after 7 days.


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

Environment variables for $CONNECTION_URL and $URL were set.

I created a database called cruddur with the command below:

```sh
CREATE database cruddur;
```

#### db-create

```sh

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-create"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<< "$CONNECTION_URL")
psql $NO_DB_CONNECTION_URL -c "create database cruddur;"
```

This was used to create the Cruddur database using the command below. Colour formatting was added using Cyan.

```sh
CREATE DATABASE Cruddur;
```

#### db-drop

```sh
CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-drop"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<< "$CONNECTION_URL")
psql $NO_DB_CONNECTION_URL -c "drop database cruddur;"
```

This can be used to drop the database Cruddur if needed using the command below.  Colour formatting was added using Cyan.

```sh
DROP DATABASE Cruddur;
```

#### db-schema-load

```sh
CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-schema-load"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

schema_path="$(realpath .)/db/schema.sql"
echo $schema_path

if [ "$1" = "prod" ]; then
  echo "Running in production mode"
  URL=$PROD_CONNECTION_URL
else
  URL=$CONNECTION_URL
fi

psql $URL cruddur < $schema_path
```

This is for loading the schema.

#### db-seed

```sh
CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-seed"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

seed_path="$(realpath .)/db/seed.sql"
echo $seed_path

if [ "$1" = "prod" ]; then
  echo "Running in production mode"
  URL=$PROD_CONNECTION_URL
else
  URL=$CONNECTION_URL
fi

psql $URL cruddur < $seed_path
```

This was used to load the seed data.


**SQL for seed data

```sh
INSERT INTO public.users (display_name, handle, cognito_user_id)
VALUES
  ('Andrew Brown', 'andrewbrown' ,'MOCK'),
  ('Andrew Bayko', 'bayko' ,'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'andrewbrown' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )
  ```
  
![seeddata](https://user-images.githubusercontent.com/78261965/226113865-6074d607-8af2-4d54-8c3d-7e7badf26265.png)

![imported as seed data](https://user-images.githubusercontent.com/78261965/226113886-b946f3af-d131-4641-9c41-3c0f185d4b63.png)


![Imported_as_seed_data](https://user-images.githubusercontent.com/78261965/226113911-7dc82985-ed05-4740-85c0-7b26f589eda8.png)

  
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


