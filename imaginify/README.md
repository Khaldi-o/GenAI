# Imaginify/Weezter

## Install and run with docker (recommended)

Requirements:

- docker and docker-compose

### Using docker for frontend development:

1. Create .env file from sample.env file:

```shell
cp sample.env .env
```

and complete the missing values (to not push on repo).

2. Run docker-compose:
   To make the services up and running:

```shell
docker compose up -d
```

Optionally, if rebuilding the docker images is necessary:

```shell
docker compose up --build -d
```

The current configuration with mounted volumes should refresh when saving a file in the repository.

To see the docker logs of the application, here is an example with a few options:

```shell
docker compose logs -f --tail 100 frontend
```

with

```shell
-f: to keep following logs
--tail 100: to print the last 100 logs
frontend: the name of the service we want to log, if no service specified then it will output all logs from all services
```

To stop the docker services:

```shell
docker compose down -v
```

### Docker serving frontend with nginx {#served-with-nginx}

Same as above, except use the following command extension to docker-compose:

```shell
-f docker-compose.nginx.yml
```

for example, to rebuild and start the services:

```shell
docker compose -f docker-compose.nginx.yml up --build
```

## Install and run locally

Note that jpg and png are tracked using git lfs. [Install git-lfs ](https://git-lfs.com/)

### backend

Ensure to have in the environment all necesssary variables (check the file sample.env)

In the initial Imaginify folder, run:

```shell
run api.py
```

### frontend

Ensure to have in the environment all necesssary variables (check the file sample.env).

Once in the frontend folder, run:

```shell
npm install
```

and

```shell
npm start
```

## How to deployment

### Pre-deployment steps (optional)

1. Build the images with the right values in .env file, cf. [paragraph how to serve with nginx](#served-with-nginx). Note that you need to build the image with the right values, including the right backend and frontend URLs. Also, sepcify a tag for this application version, which is connected to the urls values.
2. Once built, push the images on the gitlab container registry:

```shell
docker login registry.mahitahi.global.fujitsu.com
docker push registry.mahitahi.global.fujitsu.com/frontend/imaginify/frontend:APPLICATION_TAG
docker push registry.mahitahi.global.fujitsu.com/frontend/imaginify/backend:APPLICATION_TAG
```

The images will be now available to anywhere that can connect internet with the gitlab credentials.

### Alternative to the docker registry, building images on host

Run directly on the server the nginx docker-compose with the rigght environment values, cf. [paragraph how to serve with nginx](#served-with-nginx).

### Deployment steps

0. Prerequisite: install docker on the server
1. login to the gitlab container registy with your credentials:

```shell
docker login registry.mahitahi.global.fujitsu.com
```

2. Up the relevant containers:
   In the folder '/deploy',

```shell
cd deploy
cp sample.env .env
```

edit a '.env' file with the right values.
Create the network :

```shell
docker network create webgateway
```

Then run:

```shell
docker compose up -d
```

This command will pull both images and run them, you can also specify which service you want to pull and run adding its name at the end of the command, e.g.

```shell
docker compose up -d frontend
```
