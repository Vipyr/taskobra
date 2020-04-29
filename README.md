# [taskobra](https://vipyr.github.io/taskobra/) [![Build Status](https://travis-ci.org/Vipyr/taskobra.svg?branch=master)](https://travis-ci.org/Vipyr/taskobra)


## Getting Started 

First, determine your database credentials and add them to your env (for existing databases make sure these are correct, otherwise these values can be anything):

```sh
export POSTGRES_USER="<username here>"
export POSTGRES_PASSWORD="<password here>"
```

Next, start the docker container that instantiates the database:

```sh
docker-compose up --build 
```

If you need this to run in the background:
```sh
docker-compose up --build --detach 
```

Finally, start the monitor process:
```sh
python3 -m taskobra.monitor 
```

## Cleaning Up 

```sh
docker-compose stop
docker-compose rm 
docker volume rm flask-app-db
```