# Week 3 — Decentralized Authentication

## Required Homework 

### AWS Cognito Custom Pages

AWS Cognito lets you easily add user sign-up and authentication to your mobile and web apps. 

Install AWS Amplify is needed for authentication.

```sh
npm i aws-amplify --save
```
The following pages need to be amended to include the aws-amplify, const resend_code and const onsubmit codes:

```App.js```

```HomeFeedPage.js```

```ProfileInfo.js```

```SigninPage.js```

```SignupPage.js```

```ConfirmationPage.js```

```RecoverPage.js```


I created a user group called crudder-user-pool and a user called afrolatino as seen below:

![User Confirmation Status](https://user-images.githubusercontent.com/78261965/223215541-f5d605a1-48b8-4c34-8cd3-3ad13a6c33db.png).

During the livestream, we were unable to confirm the user created.

The command for user confirmation is as follows:

```sh
aws cognito-idp admin-set-user-password \
      --user-pool-id <your-user-pool-id> \
      --username <username> \
      --password <password> \
      --permanent
```

I was able to sign in to the web app using this user.

![Sign In Page screenshot](https://user-images.githubusercontent.com/78261965/223215727-2329e7f9-cd19-4883-b43f-4daa272bcfda.png)

The handle also displayed the name and preferred username as seen below:

![Logged in as name and preferred_username](https://user-images.githubusercontent.com/78261965/223216178-01881773-7a75-42ee-8c9b-b467fb069dd7.png)

The HomeFeedPage displays the **session, attributes, client, pool, signInUserSession, storage** as seen below:

![Details of Home Feed Page](https://user-images.githubusercontent.com/78261965/223219142-2e6b3c1f-5f11-412e-b7a7-70b17ae7e9bc.png)


### Verify JWT Token server side to serve authenticated API endpoints in Flask Application

I was able to authenticate myself following the instructions on the video as seen below:

![debug authenticated](https://user-images.githubusercontent.com/78261965/223822945-99646db9-9d94-44f8-a55d-26ca377420ff.png)

I was able to view the additional message in the codes visible only to authenticated users by Lore, **My dear brother, it is the humans that are the problem.**

![Hidden authentication message](https://user-images.githubusercontent.com/78261965/223823644-53d38757-69ff-44a5-9c52-8c3d0015e7f4.png)

### Improving UI Contrast & Implementing CSS Variables for Theming

Variables were set in Index.css page as follows:

```sh
:root {
  --bg: rgb(61,13,123);
  --fg: rgb(8,1,14);

  --field-border: rgb(255,255,255,0.29);
  --field-border-focus: rgb(149,0,255,1);
  --field-bg: rgb(31,31,31);
}
```

Several pages like ProfileInfo.css and DesktopNavigation.css were amended to improve the UI contrast.

![new screenshot](https://user-images.githubusercontent.com/78261965/224431567-74fd17bf-5fe8-48d7-9f4a-3d0e9c2dbd17.png)
