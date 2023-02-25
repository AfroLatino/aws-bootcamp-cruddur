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


## Push and tag an image to DockerHub 

I pushed an image called containerofcats by Adrian Cantrill and went through his Docker Fundamentals course.

Please see the screenshot of the image pushed below and the Docker hub page and share link.

![Container of Cats Screenshot](https://user-images.githubusercontent.com/78261965/220468848-4453fac4-f705-487f-818d-cba49becd952.png)

![Docker Hub Screenshot](https://user-images.githubusercontent.com/78261965/220467580-138449f7-c49f-41b5-8cdb-d8b9986d5bc0.png)

[Docker Hub Share link](https://hub.docker.com/)

[Reference - Docker Fundamentals by Adrian Cantrill](https://github.com/acantril/docker-fundamentals/blob/main/build-a-simple-containerized-application/build-a-simple-containerized-application.md)

## Use multi-stage building for a Dockerfile build

I used multi-stage docker build to compile binaries and other operations typically performed before building container images.

Multistage builds make use of one Dockerfile with multiple FROM instructions. Each of these FROM instructions is a new build stage that can COPY artifacts from the previous stages. By going and copying the build artifact from the build stage, you eliminate all the intermediate steps such as downloading of code, installing dependencies, and testing. All these steps create additional layers, and you want to eliminate them from the final image.

The build stage is named by appending AS name-of-build to the FROM instruction. The name of the build stage can be used in a subsequent FROM command by providing a convenient way to identify the source layer for files brought into the image build. The final image is produced from the last stage executed in the Dockerfile.

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

List the images to see if yours have been created.

As shown on the screenshot below, this produced a demo file of size 4.82MB and another image of 922MB

![Multi-Stage Docker Build Screenshot](https://user-images.githubusercontent.com/78261965/220471045-4abc5281-7fa4-4a59-947a-05c5ac14e45e.png)

### References

[DevOps Toolkit by Viktor Farcic & Darin Pope](https://www.youtube.com/watch?v=zpkqNPwEzac)

[Earthly Blog by Lukonde Mwila](https://earthly.dev/blog/docker-multistage/)


## Implement a healthcheck in the V3 Docker compose file

The healthcheck property is now part of the Compose Specification used by recent versions of Docker Compose. This allows a check to be configured in order to determine whether containers for a service are healthy or not.

```sh
version: '3.9'  # optional since Compose v1.27.0

services:
  kong-database:
    image: postgres:9.5
    container_name: kong-postgres
    environment:
      - POSTGRES_USER=kong
      - POSTGRES_DB=kong
      - POSTGRES_HOST_AUTH_METHOD=trust
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5

  kong-migration:
    image: kong
    container_name: kong-migration
    depends_on:
      kong-database:
        condition: service_healthy
    environment:
      - KONG_DATABASE=postgres
      - KONG_PG_HOST=kong-database
    command: kong migrations bootstrap

  kong:
    image: kong
    container_name: kong
    restart: always
    depends_on:
      kong-database:
        condition: service_healthy
      kong-migration:
        condition: service_started
    links:
      - kong-database:kong-database
    ports:
      - 8000:8000
      - 8443:8443
      - 8001:8001
      - 8444:8444
    environment:
      - KONG_DATABASE=postgres
      - KONG_PG_HOST=kong-database
      - KONG_PG_DATABASE=kong
      - KONG_ADMIN_LISTEN=0.0.0.0:8001
 ```

### Waiting for PostgreSQL to be "healthy"

The following healthcheck has been configured to periodically check if PostgreSQL is ready using the ```pg_isready``` command.

```sh
healthcheck:
  test: ["CMD-SHELL", "pg_isready"]
  interval: 10s
  timeout: 5s
  retries: 5
```

If the check is successful the container will be marked as ```healthy``` as seen below. Until then it will remain in an ```unhealthy``` state.

![V3 Docker Compose Healthy](https://user-images.githubusercontent.com/78261965/220711420-bbe31f8e-5bcd-4735-99ea-7b041a0da467.png)

Services that depend on PostgreSQL can then be configured with the depends_on parameter as follows:

```sh
depends_on:
  postgres-database:
    condition: service_healthy
```

### Waiting for PostgreSQL before starting Kong

In this complete example docker-compose waits for the PostgreSQL service to be *healthy* before starting [kong](https://konghq.com/products/kong-gateway), an open-source API gateway.

Test it out with:

```sh
docker-compose up -d
```
Wait until all services are running.

Test by querying Kong's admin endpoint:

```sh
curl http://localhost:8001/
```

See the screenshot of the result below:
![V3 Docker Compose Kong](https://user-images.githubusercontent.com/78261965/220713976-5f5f8aee-fe6c-4101-9565-1ce5b5781613.png)

Reference

[Docker Compose Healthcheck by Peter Evans](https://github.com/peter-evans/docker-compose-healthcheck)


## Research best practices of Dockerfiles and attempt to implement it in your Dockerfile 

A Docker image consists of read-only layers each of which represents a Dockerfile instruction. The layers are stacked and each one is a delta of the changes from the previous layer. The following is the contents of the Dockerfile I implemented:

```sh
# syntax=docker/dockerfile:1
FROM ubuntu:18.04
COPY . /app
RUN apt-get update && apt-get install -y \
    aufs-tools \
    automake \
    build-essential \
    curl \
    dpkg-sig \
    libcap-dev \
    libsqlite3-dev \
    mercurial \
    reprepro \
    && rm -rf /var/lib/apt/lists/*
CMD python /app/app.py
```

### General guidelines and recommendations

I have listed some general guidelines and recommendations below:

#### Create ephemeral containers

The image defined by your Dockerfile should generate containers that are as ephemeral as possible. Ephemeral means that the container can be stopped and destroyed, then rebuilt and replaced with an absolute minimum set up and configuration.

#### Minimise the number of layers

In older versions of Docker, it was important that you minimised the number of layers in your images to ensure they were performant. The following features were added to reduce this limitation:

Only the instructions RUN, COPY, ADD create layers. Other instructions create temporary intermediate images, and don’t increase the size of the build.

Where possible, use multi-stage builds, and only copy the artifacts you need into the final image. This allows you to include tools and debug information in your intermediate build stages without increasing the size of the final image.

#### Sort multi-line arguments

Whenever possible, ease later changes by sorting multi-line arguments alphanumerically. This helps to avoid duplication of packages and make the list much easier to update. Adding a space before a backslash (\) helps as well.

#### Leverage build cache

When building an image, Docker steps through the instructions in your Dockerfile, executing each in the order specified. As each instruction is examined, Docker looks for an existing image in its cache that it can reuse, rather than creating a new, duplicate image.

If you don’t want to use the cache at all, you can use the ```--no-cache=true``` option on the ```docker build``` command.

#### Use multi-stage builds

Multi-stage builds allow you to drastically reduce the size of your final image, without struggling to reduce the number of intermediate layers and files.

Because an image is built during the final stage of the build process, you can minimise image layers by leveraging build cache.

#### Exclude with .dockerignore

To exclude files not relevant to the build, without restructuring your source repository, use a .dockerignore file.

## Dockerfile Instructions

My dockerfile used the FROM, COPY, RUN and CMD commands. LABEL, CMD, EXPOSE, ENV, ENTRYPOINT, VOLUME, USER, WORKDIR, ONBUILD are other commands that can also be used.

I have written only about the RUN command below as I encountered some challenges running my dockerfile with this command.

### RUN

Dockerfile can be made more readable and understandable by splitting long or complex RUN statements on multiple lines separated with backslashes.

#### apt-get

apt-get is probably the most common use-case for RUN. Because it installs packages, the RUN apt-get command has several counter-intuitive behaviours to look out for.

Always combine RUN apt-get update with apt-get install in the same RUN statement. 

Using apt-get update alone in a RUN statement causes caching issues and subsequent apt-get install instructions fail. 

After building the image, all layers are in the Docker cache.

Docker sees the initial and modified instructions as identical and reuses the cache from previous steps. As a result, the apt-get update is not executed because the build uses the cached version. Because the apt-get update isn’t run, your build can potentially get an outdated version of the curl and nginx packages.

Using RUN apt-get update && apt-get install -y ensures your Dockerfile installs the latest package versions with no further coding or manual intervention. This technique is known as cache busting. You can also achieve cache busting by specifying a package version. This is known as version pinning. 

Version pinning forces the build to retrieve a particular version regardless of what’s in the cache. This technique can also reduce failures due to unanticipated changes in required packages

Below is a well-formed RUN instruction that demonstrates all the apt-get recommendations which I also implemented.

```sh
RUN apt-get update && apt-get install -y \
    auf-tools \
    automake \
    build-essential \
    curl \
    dpkg-sig \
    libcap-dev \
    libsqlite3-dev \
    mercurial \
    reprepro \
&& rm -rf /var/lib/apt/lists/*
```

Listing packages on each line can also prevent mistakes in package duplication.

![Docker Best Practice Screenshot](https://user-images.githubusercontent.com/78261965/220727587-c1130356-d864-4c4b-b569-ad40a930a9cb.png)

![Docker Best Practice V2](https://user-images.githubusercontent.com/78261965/220727613-b203ba23-8cdf-4401-a239-e6d9cabde51f.png)

**Reference**

[Dockerfile Best Practices Share Link](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)


## Learn how to install Docker on your local machine and get the same containers running outside of Gitpod / Codespaces

I successfully installed Docker on my local machine as seen from the screenshot below:

![Docker Desktop](https://user-images.githubusercontent.com/78261965/220754483-a97148ce-dc3f-416f-a152-eeeb34855a30.png)

I ran the docker command below on Gitpod and my local machine to get the same container

```sh
docker run -it ubuntu bash
```

**Containers running outside of Gitpod**

![Container from Gitpod](https://user-images.githubusercontent.com/78261965/220754745-30143423-072e-4066-bf2d-21006822a1ee.png)

**Containers running from my local Docker machine**

![Docker on local machine](https://user-images.githubusercontent.com/78261965/220755107-bc3c3ba4-1909-4a07-a002-082b3296fb49.png)


## Launch an EC2 instance that has docker installed, and pull a container to demonstrate you can run your own docker processes. 

I created an AWS EC2 instance as seen below:

![EC2 Instance Screenshot](https://user-images.githubusercontent.com/78261965/221367337-a7699e23-f917-47d6-928f-2cd6b751da57.png)

[Amazon EC2 Instance Share Link](https://us-east-1.console.aws.amazon.com/ec2/home?region=us-east-1#Instances:)

I configured 2 security groups of SSH and HTTP to enable me log into the instance.

I created a new key pair as this needs to be converted into .ppx file.

I took note of my Public IPv4 address and Public IPv4 DNS details as these would be needed later.

I installed PuTTY Key Generator to convert the private key to a .ppk file.

I entered my details onto PuTTY Configuration and launched the EC2 instance created.

![EC2UserInstance](https://user-images.githubusercontent.com/78261965/221367468-33ba6910-1bb0-40cd-8910-dd55149fdc26.png)

### For package update

```sh
sudo yum update -y
```

### For docker installation

```sh
sudo yum install -y docker
```

### To start the service

```sh
sudo service docker start
```

### In order to stop using sudo command

```sh
sudo usermod -a -G docker ec2-user
```

Then ```exit```. Re-enter your details through the PuTTY configuration file.

### Run Python Script

```sh
Docker info
```

```sh
docker run -d -p 80:5000 training/webapp:latest python app.py
```

### Viewing Hello World on local host using curl commans

```sh
 curl http://localhost
 ```
 
 **Create container in nginx**
 
 ```sh
 docker run -d -p 80:80 --name nginx nginx 
 ```
 
![HelloWorld_EC2Instance](https://user-images.githubusercontent.com/78261965/220784359-6d9793a9-4608-493b-8f98-4ec905d5d2aa.png)

When my Public IPv4 DNS address was added onto the browser, I was able to view Hello World as seen below:

![EC2InstanceHelloWorld](https://user-images.githubusercontent.com/78261965/220784425-dd2ecc8f-970e-43be-b667-9b6b314d9f1d.png)

**Reference**

[Launch a Docker Container On A Single EC2 instance by ITJobHacks](https://www.youtube.com/watch?v=cdqbPfGkUu4&t=3s)


