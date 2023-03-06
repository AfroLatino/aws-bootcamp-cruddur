# Week 3 — Decentralized Authentication

## Required Homework 

### AWS Cognito Custom Pages

AWS Cognito lets you easily add user sign-up and authentication to your mobile and web apps. 

Install AWS Amplify is needed for authentication.

```sh
npm i aws-amplify --save
```
The following pages need to be amended:
```App.js```
```HomeFeedPage.js```
```ProfileInfo.js```


I created a user pool called crudder-user-pool and a user called afrolatino as seen below:

![User Confirmation Status](https://user-images.githubusercontent.com/78261965/223215541-f5d605a1-48b8-4c34-8cd3-3ad13a6c33db.png).

I was able to sign in to the web app using this user.

![Sign In Page screenshot](https://user-images.githubusercontent.com/78261965/223215727-2329e7f9-cd19-4883-b43f-4daa272bcfda.png)

The handle also displayed the name and preferred username as seen below:

![Logged in as name and preferred_username](https://user-images.githubusercontent.com/78261965/223216178-01881773-7a75-42ee-8c9b-b467fb069dd7.png)
