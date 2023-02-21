# Week 1 — App Containerization

## Required Homework Challenges

I watched all the videos published and completed my tasks for the week as follows:

Gained practical knowledge working with docker commands and running container images.

Watched the security video from Ashish to know the Top 10 Docker Container Security Best Practices

Created docker-compose file

Configured Gitpod.yml configuration

Ran DynamoDB Local Container and Postgres Container to ensure they worked.

![Docker Compose Screenshot](https://user-images.githubusercontent.com/78261965/220464427-90f3b9fc-1e1f-45a8-a6a8-81b427fc6d8a.png)

[Processing Files Share Link](https://github.com/AfroLatino/aws-bootcamp-cruddur-2023)



## Stretch Homework Challenges

### Run the dockerfile CMD as an external script

### Add Dockerfile

Create a file here: `Dockerfile`

```dockerfile
FROM nginx:latest

LABEL maintainer=",<email-address>" 

COPY 2048 /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Build Container

```sh
docker build -t iis
```

![Docker CMD Screenshot](https://user-images.githubusercontent.com/78261965/220466499-b6fb2b50-3281-4ef7-889a-046cf22ad5c5.png)
