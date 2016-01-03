#!/usr/bin/env bash

PASSWORD=ccJtyF3dTplyez4v

# Ensure the docker VM is running (Mac OS X)
if [ "$(docker-machine status default)" != "Running" ]; then
    docker-machine start default
fi
eval "$(docker-machine env default)"

# Grab the latest Cassandra image
MARIADB_EXISTS=`docker images | grep mariadb >/dev/null 2>&1`
if [ "$?" != "0" ]; then
	docker pull mariadb
fi

## TODO: bind mount the tablespace for cross-build persistence
# Check to see if mdb1 exists
MDB1_EXISTS=`docker inspect --format="{{.State.Running}}" mdb1 >/dev/null 2>&1`
if [ "$?" != "0" ]; then
	docker run --name mdb1 -d -e MYSQL_ROOT_PASSWORD=${PASSWORD} -e TERM=dumb --net=host  mariadb
fi
# On the other hand, MDB1 might exist but be stopped, if so remove it first
MDB1_RUNNING=`docker inspect --format="{{.State.Running}}" mdb1`
if [ "${MDB1_RUNNING}" != "true" ]; then
	docker rm mdb1
	docker run --name mdb1 -d -e MYSQL_ROOT_PASSWORD=${PASSWORD} -e TERM=dumb --net=host mariadb
else
	printf "attempting to create schema and tables"
	## We need to give MariaDB a moment to start
	for i in {1..5}; do
	    printf "."
	    sleep 1
	done
	echo
	## This sucks. We need a mysql client on the IDE's host OS. But doing a docker cp and trying
	## to load the schema from within the container fails, probably due to TTY or something like.
	DOCKER_MACHINE=`docker-machine ls default | grep ^default | awk '{print $5}' | cut -d: -f 2 | sed -e 's/^..//'`
	mysql -h ${DOCKER_MACHINE} --port 3306 -u root --password=${PASSWORD} < ../schema.sql
fi
