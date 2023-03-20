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


### Bin Folder

I created anew folder called bin.

To give executable access to a user, type in **chmod u+x**, then the file path. See example below:

```sh
chmod u+x ./bin/db-create
```

The colour changes once this si applied.

![db_createdropschema-load](https://user-images.githubusercontent.com/78261965/226115779-0265e6e7-1319-4b1c-920f-8ea7d21acd7e.png)


To view records in a more ordered manner, you can put the expanded display on.

```sh
\x on 
```

#### db-connect

This is used for establising connection to the database. 

To access the local database, use the command below:

```sh
./bin/db-connect
```

**For Production**

```sh
./bin/db-connect prod
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

This is for loading the schema.

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

**SQL for schema**

An extension of uuid-ossp was created using IF NOT EXISTS command. This is not created if it does exist.

It also drops tables public.users and public.activities if they do exist and re-creates them.

```sh
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.activities;
CREATE TABLE public.users (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  display_name text NOT NULL,  
  handle text NOT NULL,
  email text NOT NULL,
  cognito_user_id text NOT NULL,
  created_at TIMESTAMP default current_timestamp NOT NULL
);

CREATE TABLE public.activities (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_uuid UUID NOT NULL,
  message text NOT NULL,
  replies_count integer DEFAULT 0,
  reposts_count integer DEFAULT 0,
  likes_count integer DEFAULT 0,
  reply_to_activity_uuid integer,
  expires_at TIMESTAMP,
  created_at TIMESTAMP default current_timestamp NOT NULL
);
```

#### db-seed

This was used to load the seed data.

It used $PROD_CONNECTION_URL when running in production enviroment else $CONNECTION_URL. These were set as environment variables.

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

**SQL for seed data**

This SQL command was used to insert data into public.users and public.activities tables.

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
  
 Data displayed after using the command below:
 
 ```sh 
 SELECT * from users;
 ```
 
![seeddata](https://user-images.githubusercontent.com/78261965/226113865-6074d607-8af2-4d54-8c3d-7e7badf26265.png)

Data displayed after using the command below:
 
 ```sh 
 SELECT * from activities;
 ```
 
![imported as seed data](https://user-images.githubusercontent.com/78261965/226113886-b946f3af-d131-4641-9c41-3c0f185d4b63.png)

The seed data was later viewed on the front end as seen below:

![Andrew Brown shows up](https://user-images.githubusercontent.com/78261965/226115881-c029cb98-507c-431b-a36b-581b23b330e2.png)


#### db-sessions

The command below was used to establish database connections.

```sh
CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-sessions"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

if [ "$1" = "prod" ]; then
  echo "Running in production mode"
  URL=$PROD_CONNECTION_URL
else
  URL=$CONNECTION_URL
fi

NO_DB_URL=$(sed 's/\/cruddur//g' <<<"$URL")
psql $NO_DB_URL -c "select pid as process_id, \
       usename as user,  \
       datname as db, \
       client_addr, \
       application_name as app,\
       state \
from pg_stat_activity;"
```

An example of a database session is seen below:

![db-sessions](https://user-images.githubusercontent.com/78261965/226115727-b875cefb-fb8a-4f5f-b860-b8bdefebda4a.png)

#### db-setup

```sh
CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-setup"
printf "${CYAN}==== ${LABEL}${NO_COLOR}\n"

bin_path="$(realpath .)/bin"

source "$bin_path/db-drop"
source "$bin_path/db-create"
source "$bin_path/db-schema-load"
source "$bin_path/db-seed"
```

#### rds-update-sg-rule

```sh
CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="rds-update-sg-rule"
printf "${CYAN}==== ${LABEL}${NO_COLOR}\n"

aws ec2 modify-security-group-rules \
    --group-id $DB_SG_ID \
    --security-group-rules "SecurityGroupRuleId=$DB_SG_RULE_ID,SecurityGroupRule={Description=GITPOD,IpProtocol=tcp,FromPort=5432,ToPort=5432,CidrIpv4=$GITPOD_IP/32}"
```

### Setup Cognito post confirmation lambda

A lambda trigger was set up in the user pool created using Python 3.8.

AWS Lambda is a compute service that lets you run code without provisioning or managing servers. Lambda runs your code on a high-availability compute infrastructure and performs all of the administration of the compute resources, including server and operating system maintenance, capacity provisioning and automatic scaling, and logging. With Lambda, you can run code for virtually any type of application or backend service.

**When to use Lambda**

Lambda is an ideal compute service for many application scenarios, as long as you can run your application code using the Lambda standard runtime environment and within the resources that Lambda provides. You can use Lambda for:

**Web applications:** Combine Lambda with other AWS services to build powerful web applications that automatically scale up and down and run in a highly available configuration across multiple data centers.


![cruddurpostconfirm](https://user-images.githubusercontent.com/78261965/226115220-adf1ed74-4b59-4637-b955-9638aeac5d1f.png)

**Reference**

[AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)


#### Creating Users

I was able to create a user and search for this in Production.

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

#### Updating Crud

I was able to update Crud with my posts.

![Crudscreenshot](https://user-images.githubusercontent.com/78261965/226364943-0472a911-e1ad-4c0b-988f-dc94bc9e0e70.png)


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


