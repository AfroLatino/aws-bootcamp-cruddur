# Week 5 — DynamoDB and Serverless Caching

## Required Homework 

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

Internet Gateway

VPC/Gateway Endpoints

DynamoDB Accelerator (DAX)

Cross Account

### Creating a DynamoDB table

DynamoDB is a key value pair. Keys are usually partition or sort keys and are unique identifiers. Customers are charged by Read (RCU) and Write Capacity (WCU). Ensure deletion protection is on as this is off by default. It is important to have tags to identify the streams the tables belong to. 

Regional endpoints are used to make requests. The general syntax of a regional endpoint is as follows:

$\color{red}{protocol://service-code.region-code}$.awazonaws.com

$$\color{BurntOrange}{MBurntOrange}$$





