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

[DevOps Toolkit](https://www.youtube.com/watch?v=zpkqNPwEzac)

[Earthly Blog](https://earthly.dev/blog/docker-multistage/)


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

The following healthcheck has been configured to periodically check if PostgreSQL is ready using the pg_isready command.

```sh
healthcheck:
  test: ["CMD-SHELL", "pg_isready"]
  interval: 10s
  timeout: 5s
  retries: 5
```

If the check is successful the container will be marked as healthy as seen below. Until then it will remain in an unhealthy state.

![V3 Docker Compose Healthy](https://user-images.githubusercontent.com/78261965/220711420-bbe31f8e-5bcd-4735-99ea-7b041a0da467.png)


