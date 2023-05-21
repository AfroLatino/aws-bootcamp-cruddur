# Week X — Tidying up the codes

## Table of contents
- [Introduction](#introduction)
- [Sync tool for static website hosting](#paragraph1)
- [Reconnect Database and Post Confirmation Lambda](#paragraph2)
- [Use CORS for Service](#paragraph3)
- [CICD Pipeline and Create Activity](#paragraph4)
- [Refactor JWT to use a decorator](#paragraph5)
- [Refactor AppPy](#paragraph6)
- [Refactor Flask Routes](#paragraph7)
- [Replies Work In Progress](#paragraph8)
- [Refactor Error Handling and Fetch Requests](#paragraph9)
- [Activity Show Page](#paragraph10)


### Introduction  <a name="introduction"></a>

This was the final week of cleaning up all the codes from the app to make them more readable and efficient.


### Sync tool for static website hosting <a name="paragraph1"></a>

Create a new file called ```static-build``` within bin / frontend folder with the command below:

```sh
#! /usr/bin/bash

ABS_PATH=$(readlink -f "$0")
FRONTEND_PATH=$(dirname $ABS_PATH)
BIN_PATH=$(dirname $FRONTEND_PATH)
PROJECT_PATH=$(dirname $BIN_PATH)
FRONTEND_REACT_JS_PATH="$PROJECT_PATH/frontend-react-js"

cd $FRONTEND_REACT_JS_PATH

REACT_APP_BACKEND_URL="https://api.ocubeltd.co.uk" \
REACT_APP_AWS_PROJECT_REGION="$AWS_DEFAULT_REGION" \
REACT_APP_AWS_COGNITO_REGION="$AWS_DEFAULT_REGION" \
REACT_APP_AWS_USER_POOLS_ID="$AWS_COGNITO_AWS_USER_POOL_ID" \
REACT_APP_CLIENT_ID="$AWS_COGNITO_AWS_USER_POOL_CLIENT_ID" \
npm run build
```

Amend ```frontend-react-js/src/pages/SigninPage.js``` with parts of the command below:

```sh
const onsubmit = async (event) => {
    setErrors('')
    event.preventDefault();
    Auth.signIn(email, password)
    .then(user => {
      console.log('user',user)
      localStorage.setItem("access_token", user.signInUserSession.accessToken.jwtToken)
      window.location.href = "/"
    })
    .catch(error => { 
      if (error.code === 'UserNotConfirmedException') {
        window.location.href = "/confirm"
      }
      setErrors(error.message)
    });
    return false
  }
```

Amend ```frontend-react-js/src/components/ActivityContent.css``` by adding flex-start to align-items with parts of the command below:

```sh
.activity_content_wrap {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
}
```

Amend ```frontend-react-js/src/pages/RecoverPage.js``` with parts of the command below:

```sh
const onsubmit_confirm_code = async (event) => {
    event.preventDefault();
    setErrors('')
    if (password === passwordAgain){
      Auth.forgotPasswordSubmit(username, code, password)
      .then((data) => setFormState('success'))
      .catch((err) => setErrors(err.message) );
    } else {
      setErrors('Passwords do not match')
    }
    return false
  }
  
  ---
  
  let form;
  if (formState === 'send_code') {
    form = send_code()
  }
  else if (formState === 'confirm_code') {
    form = confirm_code()
  }
  else if (formState === 'success') {
    form = success()
  }
```

Amend ```frontend-react-js/src/pages/ConfirmationPage.js``` with parts of the command below:

```sh
const resend_code = async (event) => {
    setErrors('')
    try {
      await Auth.resendSignUp(email);
      console.log('code resent successfully');
      setCodeSent(true)
    } catch (err) {
      // does not return a code
      // does cognito always return english
      // for this to be an okay match?
      console.log(err)
      if (err.message === 'Username cannot be empty'){
        setErrors("You need to provide an email in order to send Resend Activiation Code")   
      } else if (err.message === "Username/client id combination not found."){
        setErrors("Email is invalid or cannot be found.")   
      }
    }
  }
```

Amend ```frontend-react-js/src/components/ProfileInfo.js``` with parts of the command below:

```sh
const classes = () => {
    let classes = ["profile-info-wrapper"];
    if (popped === true){
      classes.push('popped');
    }
    return classes.join(' ');
  }
```

Amend ```frontend-react-js/src/components/ProfileForm.js``` with parts of the command below:

```sh
let data = await res.json();
      if (res.status === 200) {
        return data.url
      } else {
        console.log(res)
      }
    } catch (err) {
      console.log(err);
 ```

Comment out codes not being used as follows:

```sh
//let data = await res.json();

--

//const preview_image_url = URL.createObjectURL(file)
```

