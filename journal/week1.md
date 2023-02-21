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

Creat a file called `Dockerfile`

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

### Container successfully built and tagged

![Docker CMD Screenshot](https://user-images.githubusercontent.com/78261965/220466499-b6fb2b50-3281-4ef7-889a-046cf22ad5c5.png)


## Push and tag a image to DockerHub 

I pushed an image called containerofcats by Adrian Cantrill and went through his Docker Fundamentals course.

Please see the screenshot of the image pushed below and the Docker hub page and share link.

![Container of Cats Screenshot](https://user-images.githubusercontent.com/78261965/220468848-4453fac4-f705-487f-818d-cba49becd952.png)

![Docker Hub Screenshot](https://user-images.githubusercontent.com/78261965/220467580-138449f7-c49f-41b5-8cdb-d8b9986d5bc0.png)

[Docker Hub Share link](https://hub.docker.com/)

[Reference - Docker Fundamentals by Adrian Cantrill](https://github.com/acantril/docker-fundamentals/blob/main/build-a-simple-containerized-application/build-a-simple-containerized-application.md)

## Use multi-stage building for a Dockerfile build

I used multi-stage docker build to compile binaries and other operations typically performed before building container images.

### Add Dockerfile

Creat a file called `Dockerfile`

```Dockerfile
FROM golang:1.16 AS build
ADD . /src
WORKDIR /src


FROM alpine:3.4
EXPOSE 8080
CMD ["demo"]
```

### Build Container

```sh
docker image build --tag  demo .
```

### List Images

```sh
docker image list
```

List the images to view if yours have been created

As shown on the screenshot below, this produced a demo file of size 4.82MB and another image of 922MB

![Multi-Stage Docker Build Screenshot](https://user-images.githubusercontent.com/78261965/220471045-4abc5281-7fa4-4a59-947a-05c5ac14e45e.png)

[Reference - DevOps Toolkit](https://www.youtube.com/watch?v=zpkqNPwEzac)
