# Deployment Model

## Deploying the Database and Webserver

First step in deploying is to deploy the Webservice! 
    
This comes with a built in database that it will automatically set up and configure, however if you would like to set up and deploy a database seperately, see the instructions below. 

```sh
docker run -e OAUTH_API_URL=<URL> -e OAUTH_API_KEY=<KEY> vipyr/taskobra:latest
```

## Deploying a Database Seperately 

There are two main ways to deploy a database seperately, either with a 'Database as a Service' or as a standalone installation.

#### Database as a Service Providers

[Amazon AWS](https://aws.amazon.com/rds/postgresql/)

[Microsoft Azure](https://azure.microsoft.com/en-us/services/postgresql/)

#### Standalone Database Installation

[PostgreSQL](https://www.postgresql.org/docs/10/tutorial-start.html)

[Official Docker Image for PostgreSQL](https://github.com/docker-library/postgres)

#### Running the Daemon with an External DB

```sh
docker run -e OAUTH_API_URL=<URL> -e OAUTH_API_KEY=<KEY>\
           -e DATABASE_URL=<URL> -e DATABASE_URL=<KEY>\
           vipyr/taskobra:latest
```


## Running the Daemon 

Once the Webservice is deployed, the only thing left to do is start the Daemon on any hosts! 
    
The Daemons will automatically call home to the webserver that you specify by connecting to the database and you'll be able to start using your Taskobra installation immediately. 

```sh
# Install the Daemon into the Python Installation
git clone git@github.com:Vipyr/taskobra.git
cd taskobra && python3 setup.py install 

# Run the Daemon! 
DATABASE_URL=<URL> DATABASE_KEY=<KEY> python -m taskobra
```


