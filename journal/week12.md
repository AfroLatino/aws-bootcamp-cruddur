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

Amend ```frontend-react-js/src/components/MessageGroupItem.js``` with parts of the command below:

```sh
  const classes = () => {
    let classes = ["message_group_item"];
    if (params.message_group_uuid === props.message_group.uuid){
      classes.push('active')
    }
    return classes.join(' ');
  }
 ```
 
 Amend ```frontend-react-js/src/components/MessageForm.js``` by adding the code below:
 
 ```sh
 import { useParams } from 'react-router-dom';
 ```
 
 Amend ```frontend-react-js/src/components/DesktopSidebar.js``` with parts of the command below:
 
 ```sh
   return (
    <section>
      <Search />
      {trending}
      {suggested}
      {join}
      <footer>
        <a href="/about">About!</a>
        <a href="/terms-of-service">Terms of Service</a>
        <a href="/privacy-policy">Privacy Policy</a>
      </footer>
    </section>
  );
}
```

Amend ```frontend-react-js/src/components/DesktopNavigationLink.js``` with parts of the command below:

```sh
 const icon = ()=> {
    switch(props.handle){
      case 'home':
        return <HomeIcon className='icon' />
        break;
      case 'notifications':
        return <NotificationsIcon className='icon' />
        break;
      case 'profile':
        return <ProfileIcon className='icon' />
        break;
      case 'more':
        return <MoreIcon className='icon' />
        break;
      case 'messages':
        return <MessagesIcon className='icon' />
        break;
      default: 
        break;
    }
  }
```

Amend ```frontend-react-js/src/components/MessageGroupItem.css``` with parts of the command below:

```sh
.message_group_item {
  display: flex;
  align-items: flex-start;
  overflow: hidden;
  padding: 16px;
  cursor: pointer;
  text-decoration: none;
}
```

Amend ```frontend-react-js/src/components/MessageItem.css``` with parts of the command below:

```sh
.message_item {
  display: flex;
  align-items: flex-start;
  overflow: hidden;
  border-bottom: solid 1px rgb(31,36,49);
  padding: 16px;
  cursor: pointer;
  text-decoration: none;
}
```

Amend ```frontend-react-js/src/components/ProfileHeading.css``` with parts of the command below:

```sh
.profile_heading .info {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  padding: 16px;
}
```

Amend ```frontend-react-js/src/components/MessageGroupItem.js``` with parts of the command below:

```sh
const classes = () => {
    let classes = ["message_group_item"];
    if (params.message_group_uuid === props.message_group.uuid){
      classes.push('active')
    }
    return classes.join(' ');
  }
```

Run the command below in the frontend-flask directory; ```/workspace/aws-bootcamp-cruddur-2023/frontend-react-js``` to build the application:

```sh
REACT_APP_BACKEND_URL="https://api.ocubeltd.co.uk" \
REACT_APP_AWS_PROJECT_REGION="$AWS_DEFAULT_REGION" \
REACT_APP_AWS_COGNITO_REGION="$AWS_DEFAULT_REGION" \
REACT_APP_AWS_USER_POOLS_ID="$AWS_USER_POOLS_ID" \
REACT_APP_CLIENT_ID="$APP_CLIENT_ID" \
npm run build
```

Zip the contents by running the command below:

```sh
zip -r build.zip build/
```

- This creates the build.zip file
- Right click and download the file
- Delete the build.zip file from the directory.
- Navigate to Amazon S3 -> Buckets -> ocubeltd.co.uk
- Copy the build zip folder onto the desktop
- Open the build folder
- Copy and drag all the contents onto the page
- Click on upload

I typed ocubeltd.co.uk on the URL and got the web application as seen below:

![ocubeltd co uk_webapplication_showing](https://github.com/AfroLatino/aws-bootcamp-cruddur-2023/assets/78261965/b8ccfb18-bb04-4b07-bd28-13d19762ea43)

Create a file called ```sync``` within ```bin / frontend``` directory with the command below:

```sh
#!/usr/bin/env ruby

require 'aws_s3_website_sync'
require 'dotenv'

env_path = "/workspace/aws-bootcamp-cruddur-2023/sync.env"
Dotenv.load(env_path)

puts "== configuration"
puts "aws_default_region:   #{ENV["AWS_DEFAULT_REGION"]}"
puts "s3_bucket:            #{ENV["SYNC_S3_BUCKET"]}"
puts "distribution_id:      #{ENV["SYNC_CLOUDFRONT_DISTRUBTION_ID"]}"
puts "build_dir:            #{ENV["SYNC_BUILD_DIR"]}"

changeset_path = ENV["SYNC_OUTPUT_CHANGESET_PATH"]
changeset_path = changeset_path.sub(".json","-#{Time.now.to_i}.json")

puts "output_changset_path: #{changeset_path}"
puts "auto_approve:         #{ENV["SYNC_AUTO_APPROVE"]}"

puts "sync =="
AwsS3WebsiteSync::Runner.run(
  aws_access_key_id:     ENV["AWS_ACCESS_KEY_ID"],
  aws_secret_access_key: ENV["AWS_SECRET_ACCESS_KEY"],
  aws_default_region:    ENV["AWS_DEFAULT_REGION"],
  s3_bucket:             ENV["SYNC_S3_BUCKET"],
  distribution_id:       ENV["SYNC_CLOUDFRONT_DISTRUBTION_ID"],
  build_dir:             ENV["SYNC_BUILD_DIR"],
  output_changset_path:  changeset_path,
  auto_approve:          ENV["SYNC_AUTO_APPROVE"],
  silent: "ignore,no_change",
  ignore_files: [
    'stylesheets/index',
    'android-chrome-192x192.png',
    'android-chrome-256x256.png',
    'apple-touch-icon-precomposed.png',
    'apple-touch-icon.png',
    'site.webmanifest',
    'error.html',
    'favicon-16x16.png',
    'favicon-32x32.png',
    'favicon.ico',
    'robots.txt',
    'safari-pinned-tab.svg'
  ]
)
```

In the main directory, install gem by running the command below:

```sh
gem install aws_s3_website_sync
```

Create a new file within ```erb``` in the main directory called ```sync.env.erb``` with the command below:

```sh
SYNC_S3_BUCKET=$SYNC_S3_BUCKET
SYNC_CLOUDFRONT_DISTRIBUTION_ID=$SYNC_CLOUDFRONT_DISTRIBUTION_ID 
// This is the distribution ID for Frontend React JS for Cruddur
SYNC_BUILD_DIR=<%= ENV['THEIA_WORKSPACE_ROOT'] %>/frontend-react-js/build
SYNC_OUTPUT_CHANGESET_PATH=<%=  ENV['THEIA_WORKSPACE_ROOT'] %>/tmp
SYNC_AUTO_APPROVE=false
```

Amend ```bin/ frontend/ generate-env``` as follows:

```sh
#!/usr/bin/env ruby

require 'erb'

template = File.read 'erb/frontend-react-js.env.erb'
content = ERB.new(template).result(binding)
filename = "frontend-react-js.env"
File.write(filename, content)

template = File.read 'erb/sync.env.erb'
content = ERB.new(template).result(binding)
filename = "sync.env"
File.write(filename, content)
```

Gem install env by using the command below:

```sh
gem install dotenv
```

Make sync file executable by running ```chmod u+x ./bin/frontend/sync```

Then run ```./bin/frontend/sync```

Create a ```tmp``` folder in the main directory and add a file called ```.keep```


#### Adding github actions
