# Simple-app-with-MySQL-in-docker-swarm-cluster

This is a flask based application that connects with mysql  which is deployed using a docker stack. The flask application is Loadbalanced using Traefik with a letsencrypt SSL

<br>

## Table of Contents

- [Docker Swarm Setup](#docker-swarm-setup)
- [Creating a Simple Flask-based Application That Connects with MySQL](#creating-a-simple-flask-based-application-that-connects-with-mysql)
- [Deploying the Docker Stack](#deploying-the-docker-stack)
- [Manually Adding Random SQL Queries Inside a Table](#manually-adding-random-sql-queries-inside-a-table)
- [Accessing the Application](#accessing-the-application)


<br>
### Docker swarm setup ###
***

I'm using an AWS free-tier setup with the instance selected as t2.micro, the docker architecture will have one manager node and 3 worker nodes. The docker is installed using an userdata script that will install docker once the ec2-instance is provisioned.


```sh
#!/bin/bash

yum install docker -y
systemctl start docker
systemctl enable docker
usermod -aG docker ec2-user
su - ec2-user

```

After installing the docker I've changed the hostname of the nodes so that it would be user-friendly to read.
```sh
sudo hostnamectl set-hostname manager/worker<ap-south.internal>
```
My docker swarm architecture will look like this after changing the hostname
```sh
$ docker node ls
ID                            HOSTNAME                              STATUS    AVAILABILITY   MANAGER STATUS   ENGINE VERSION
l1f2f3gpg3lmewwckxfhykc41 *   manager.ap-south-1.compute.internal   Ready     Active         Leader           20.10.25
xlk93n6334aaorc1iy21uwhl6     worker1.ap-south-1.compute.internal   Ready     Active                          20.10.25
91zcx5peka2kb2ruc38ueu2eq     worker2.ap-south-1.compute.internal   Ready     Active                          20.10.25
z6tyoxmdw2vb6yfvycaw7gx0p     worker3.ap-south-1.compute.internal   Ready     Active                          20.10.25
```



### A simple flask based application that connects with mysql
***

After installing the docker then I created a Flask based application that connects Flask with mysql, which displays the ```SELECT * FROM <table_name> ``` sql query while loading the application in web browser. I've designed the application in such a way that an index.html page is rendered which is by-default is placed in the ***templates directory*** and the credintials required to connect to mysql are fetched from an ***environnment variable***.

Once that's set, I've created a Dockerfile that dockerise the application which later pushed to my dockerhub account
```sh

# docker login to your docker-hub account
docker login

# docker image build from dockerfile and using the name 
docker image build -t chrisluiz16/flask-mysql:latest .

# pushing it to the your account as a public image
docker image push chrisluiz16/flask-mysql:latest

```

I have created ```.dockerignore``` file so that only application based files are copied to the image.


### Deploying the docker stack

It's time to deploy the docker stack to initialize the docker swarm, before that we need to add labels to the nodes so that the services would be placed in the correct instance or nodes.

```sh
docker node update --label-add service=traefik manager.ap-south-1.compute.internal
docker node update --label-add service=flask worker1.ap-south-1.compute.internal
docker node update --label-add service=flask worker2.ap-south-1.compute.internal
docker node update --label-add service=mysql worker3.ap-south-1.compute.internal
```

I've used the domain ```sparkchrisich.tech``` to check the load-balancing of the application and ```dashboard.chrisich.tech``` to load the traefik dashboard thereby I've pointed the A record to the manager's node public IP.


git clone to a directory
```sh
git clone ssh://git@sparklabs.in:29875/christest/Simple-app-with-MySQL-in-docker-swarm-cluster.git project
cd project
```

Make sure to change the permission of ***acme.json file*** in letsencrypt directory

```sh
chmod 600 letsencrypt/acmes.json
```

Before deploying the application, I've created a custom network ```spark-net``` with the driver set as overlay

```sh
docker network create spark-net --driver=overlay 
```

Once all is set, time to deploy the application using the below command

```sh
docker stack deploy -c flask-sql.yml flask
docker stack deploy -c traefik.yml traefik
```

### Manually adding random sql queries inside a table

Once the docker stack is deployed we need to add some random queries inside the running mysql container so that the flask based application will display the SELECT query. The mysql container will be running on ```worker3.ap-south-1.compute.internal``` as I've added a label before.


Ssh into the worker node and get the container-id then exec into the container
```sh
# Login to the worker node and then exec into container
docker container ls
docker container exec -it <container id> sh
```
After exec into the container then use the below credintials to get inside the mysql
```sh
mysql -u root -pmysqlroot123
```
Last and final step would be creating a TABLE and addding some queries inside
```sql
USE college;


CREATE TABLE employees(id int(5),name varchar(255), age int (3),email varchar(255));
INSERT INTO employees (id, name,age,email) VALUES(101,"alex",30,"alex@gmail.com");
INSERT INTO employees (id, name,age,email) VALUES(102,"don",20,"don@gmail.com");
INSERT INTO employees (id, name,age,email) VALUES(103,"kevin",25,"kevin@gmail.com");
INSERT INTO employees (id, name,age,email) VALUES(103,"devon",35,"devon@gmail.com");
INSERT INTO employees (id, name,age,email) VALUES(104,"john",42,"john@gmail.com");
INSERT INTO employees (id, name,age,email) VALUES(105,"ron",38,"ron@gmail.com");
INSERT INTO employees (id, name,age,email) VALUES(106,"thomas",19,"thomas@gmail.com");
```
### Accessing the Application
After following all the above instructions, just login to ```https://spark.chrisich.tech``` and to login to traefik dashboard, you can login to ```https://dashboard.chrisich.tech```