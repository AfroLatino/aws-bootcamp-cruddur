# Week 5 — DynamoDB and Serverless Caching

## Required Homework 

### DynamoDB Utility Scripts

boto3 was added to the requirements.txt file.

To install boto3, **run pip install -r requirements.txt**.

### Creating Users

I created an extra user on Cognito called londo in addition to AfroLatino to replace existing users of Andrew and Bayko in order to view the messages.

![2users](https://user-images.githubusercontent.com/128761840/227457939-7d043426-fe38-4985-971c-4f8bd9e17ad3.png)

The CLI commands below are used for extracting Cognito Users and their attributes

```sh
aws cognito-idp list-users --user-pool-id <value>
```

```sh
aws cognito-idp list-users --user-pool-id <value> --output table
```

```
aws cognito-idp list-users --user-pool-id <value> --query Users[].Attributes
```  

### Ddb Folder

I created a new folder called ddb.

To give executable access to a user, type in **chmod u+x**, then the file path. See example below:

```sh
chmod u+x ./bin/db-create
```  

#### Drop

This is used for dropping an existing table if needed.

The sql has a command of DROP TABLE IF EXISTS.

```sh
#! /usr/bin/bash

set -e # stop if it fails at any point

if [ -z "$1" ]; then
  echo "No TABLE_NAME argument supplied eg ./bin/ddb/drop cruddur-messages prod "
  exit 1
fi
TABLE_NAME=$1

if [ "$2" = "prod" ]; then
  ENDPOINT_URL=""
else
  ENDPOINT_URL="--endpoint-url=http://localhost:8000"
fi

echo "deleting table: $TABLE_NAME"

aws dynamodb delete-table $ENDPOINT_URL \
  --table-name $TABLE_NAME
```

#### List-tables

This was for listing out the tables and very helpful to check if the table is existent.

The table used is cruddur-messages.

```sh
#! /usr/bin/bash
set -e # stop if it fails at any point

if [ "$1" = "prod" ]; then
  ENDPOINT_URL=""
else
  ENDPOINT_URL="--endpoint-url=http://localhost:8000"
fi

aws dynamodb list-tables $ENDPOINT_URL \
--query TableNames \
--output table
```

An environment variable called AWS_ENDPOINT_URL was set and added to the docker-compose file.

#### Scan

```sh
#!/usr/bin/env python3

import boto3

attrs = {
  'endpoint_url': 'http://localhost:8000'
}
ddb = boto3.resource('dynamodb',**attrs)
table_name = 'cruddur-messages'

table = ddb.Table(table_name)
response = table.scan()

items = response['Items']
for item in items:
  print(item)
```

This can be used to drop the database Cruddur if needed using the command below.  Colour formatting was added using Cyan.

```sh
DROP DATABASE Cruddur;
```

#### Schema-load

This was for loading the schema.

The Global Secondary Indexes were added to the schema-load. 

The attribute name was also added to the attribute definitions of the main table.

```sh
#!/usr/bin/env python3

import boto3
import sys

attrs = {
  'endpoint_url': 'http://localhost:8000'
}

if len(sys.argv) == 2:
  if "prod" in sys.argv[1]:
    attrs = {}

ddb = boto3.client('dynamodb',**attrs)

table_name = 'cruddur-messages'

response = ddb.create_table(
  TableName=table_name,
  AttributeDefinitions=[
    {
      'AttributeName': 'message_group_uuid',
      'AttributeType': 'S'
    },
    {
      'AttributeName': 'pk',
      'AttributeType': 'S'
    },
    {
      'AttributeName': 'sk',
      'AttributeType': 'S'
    },
  ],
  KeySchema=[
    {
      'AttributeName': 'pk',
      'KeyType': 'HASH'
    },
    {
      'AttributeName': 'sk',
      'KeyType': 'RANGE'
    },
  ],
  GlobalSecondaryIndexes= [{
    'IndexName':'message-group-sk-index',
    'KeySchema':[{
      'AttributeName': 'message_group_uuid',
      'KeyType': 'HASH'
    },{
      'AttributeName': 'sk',
      'KeyType': 'RANGE'
    }],
    'Projection': {
      'ProjectionType': 'ALL'
    },
    'ProvisionedThroughput': {
      'ReadCapacityUnits': 5,
      'WriteCapacityUnits': 5
    },
  }],
  BillingMode='PROVISIONED',
  ProvisionedThroughput={
      'ReadCapacityUnits': 5,
      'WriteCapacityUnits': 5
  }
)

print(response)
```

**Seed

The seed data was restricted to a limit of 20 characters.

Messages and message groups were created onto the seed.

```sh
def create_message_group(client,message_group_uuid, my_user_uuid, last_message_at=None, message=None, other_user_uuid=None, other_user_display_name=None, other_user_handle=None):
  table_name = 'cruddur-messages'
  record = {
    'pk':   {'S': f"GRP#{my_user_uuid}"},
    'sk':   {'S': last_message_at},
    'message_group_uuid': {'S': message_group_uuid},
    'message':  {'S': message},
    'user_uuid': {'S': other_user_uuid},
    'user_display_name': {'S': other_user_display_name},
    'user_handle': {'S': other_user_handle}
  }

  response = client.put_item(
    TableName=table_name,
    Item=record
  )
  print(response)

def create_message(client,message_group_uuid, created_at, message, my_user_uuid, my_user_display_name, my_user_handle):
  table_name = 'cruddur-messages'
  record = {
    'pk':   {'S': f"MSG#{message_group_uuid}"},
    'sk':   {'S': created_at },
    'message_uuid': { 'S': str(uuid.uuid4()) },
    'message': {'S': message},
    'user_uuid': {'S': my_user_uuid},
    'user_display_name': {'S': my_user_display_name},
    'user_handle': {'S': my_user_handle}
  }
  # insert the record into the table
  response = client.put_item(
    TableName=table_name,
    Item=record
  )
  # print the response
  print(response)

message_group_uuid = "5ae290ed-55d1-47a0-bc6d-fe2bc2700399" 
now = datetime.now(timezone.utc).astimezone()
users = get_user_uuids()

create_message_group(
  client=ddb,
  message_group_uuid=message_group_uuid,
  my_user_uuid=users['my_user']['uuid'],
  other_user_uuid=users['other_user']['uuid'],
  other_user_handle=users['other_user']['handle'],
  other_user_display_name=users['other_user']['display_name'],
  last_message_at=now.isoformat(),
  message="this is a filler message"
)

create_message_group(
  client=ddb,
  message_group_uuid=message_group_uuid,
  my_user_uuid=users['other_user']['uuid'],
  other_user_uuid=users['my_user']['uuid'],
  other_user_handle=users['my_user']['handle'],
  other_user_display_name=users['my_user']['display_name'],
  last_message_at=now.isoformat(),
  message="this is a filler message"
)
```

**SQL for seed data**

This SQL command was used to insert data into public.users and public.activities tables.

```sh
INSERT INTO public.users (display_name, email, handle, cognito_user_id)
VALUES
  ('AfroLatino','aafrolatino@test.com' , 'AfroLatino' ,'MOCK'),
  ('londo','bayko@exampro.co' , 'londo' ,'MOCK');
  
INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'afrolatino' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )
  ```
  
 Schema-load was run to load the schema, then .bin/ddb/seed was run in order to view the seed data on the front-end application
  
![seeded mesage now showing](https://user-images.githubusercontent.com/128761840/227462257-51139951-69b7-4507-b4d1-f79240ca57cf.png)

#### Patterns

2 queries for get-onversation and list-conversations were created to view the conversations.

This was run by using ./bin/ddb/patterns/get-conversations



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

this can be entered into cli to extract Cognito User  and their attributes
```sh
aws cognito-idp list-users --user-pool-id <value>
```

aws cognito-idp list-users --user-pool-id <value> --output table

aws cognito-idp list-users --user-pool-id <value> --query Users[].Attributes


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


### Amazon DynamoDB Security Best Practices

DynamoDB is a non-relational database (NoSQL). 

Customers rely on DynamoDB to support their mission-critical workloads. Amazon DynamoDB is a managed service provided by Amazon. Amazon takes care of the infrastructure and maintenance. Customers have to think of how to access DynamoDB and data to enter into it. Ensure you create a data in your region.

### DynamoDB use cases by Industry

- Banking and Finance – Fraud detection, User transactions and Mainframe offloading. Companies that use this are Capital One, Vanguard and Fannie Mae.

- Gaming – Game states, Leaderboards and Player data stores. Companies that use this are Riot Games, Electronic Arts and Penny Pop.

- Software and internet – Metadata caches, Ride-tracking data stores and Relationship graph data stores. Companies that use this are Uber, Lyft, Swiggy, Snap and Duolingo.

- Adtech – User profile stores, Metadata stores for assets and Popular-item cache. Companies that use this are AdRoll, GumGum, Branch and DataXu.

- Retail – Shopping carts, Workflow engines and Customer profiles. Companies that use this are Nordstrom, Nike, Zalando and Mercado Libre.

- Media & Entertainment – User data stores, Media metadata stores and Digital rights management stores. Companies that use this are Airtel Wynk, Amazon Prime and Netflix.

### Types of Access to DynamoDB

- Internet Gateway

- VPC/Gateway Endpoints

- DynamoDB Accelerator (DAX)

- Cross Account

### Creating a DynamoDB table

DynamoDB is a key value pair. Keys are usually partition or sort keys and are unique identifiers. Customers are charged by Read (RCU) and Write Capacity (WCU). Ensure deletion protection is on as this is off by default. It is important to have tags to identify the streams the tables belong to. 

Regional endpoints are used to make requests. The general syntax of a regional endpoint is as follows:

*Protocol://service-code.region-code*.awazonaws.com

When creating DAX Clusters, this has cost implication, so be mindful of this.

There are 2 sides to Security Best Practices for Amazon managed services. These are Amazon side and Client Application Side.

#### Amazon DynamoDB - Security Best Practices - AWS

- Use VPC Endpoints: Use Amazon Virtual Private Cloud (VPC) to create a private network from your application or Lambda to a DynamoDB. This helps to prevent authorised access to your instance from the public internet.

-	Compliance standard is what your business requires.

-	Amazon DynamoDB should only be in the AWS region that you are legally allowed to be holding user data in.

-	Amazon Organisations SCP – to manage DynamoDB table deletion, DynamoDB creation, region lock etc.

-	AWS CloudTrail is enabled and monitored to trigger alerts on malicious DynamoDB behaviour by an identity in AWS.

-	AWS Config Rules (as no GuardDuty even in March 2023) is enabled in the account and region of DynamoDB.

#### Amazon DynamoDB - Security Best Practices – Application

- DynamoDB to use appropriate Authentication – Use IAM Roles/AWS Cognito Identity Pool – Avoid IAM Users/Groups.

-	DynamoDB User Lifecyle Management – Create, Modify and Delete Users.

-	AWS IAM roles instead of individual users to access and manage DynamoDB.

-	DAX Service (IAM) Role to have Read Only Access to DynamoDB (if possible).

-	Not have DynamoDB be accessed from the internet (use VPS Endpoints etc).

-	Site to Site VPN or Direct Connect for OnPremise and DynamoDB access.

-	Client side encryption is recommended by Amazon for DynamoDB.





