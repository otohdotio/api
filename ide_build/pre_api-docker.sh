#!/usr/bin/env bash

# Ensure the docker VM is running (Mac OS X)
if [ "$(docker-machine status default)" != "Running" ]; then
    docker-machine start default
fi
eval "$(docker-machine env default)"

DOCKER_IP=`echo $DOCKER_HOST | cut -d ':' -f 2 | tr -d '/'`

# Create an SSH tunnel on 443 to the docker-machine
ps -ef | grep -v grep |  grep 443:localhost:443
if [ "$?" != "0" ]; then
    sudo ssh -f -T -N -L443:localhost:443 -l docker \
      -i ~/.docker/machine/machines/default/id_rsa \
      ${DOCKER_IP}
fi

# Kill and remove any existing api containers
# Note the -I argument to xargs is for Mac OS X compatibility
docker ps | grep otoh.io-api | awk '{print $1}' | xargs -I {} docker kill {}
docker ps -a | grep otoh.io-api | awk '{print $1}' | xargs -I {} docker rm {}

CASSANDRA=`docker inspect --format "{{ .NetworkSettings.IPAddress }}" cs1`
MDB_SERVER=${DOCKER_IP} # Because we're using host networking for now
PASSWORD=ccJtyF3dTplyez4v

printf "{ \"AttachStdin\" : false, \"Env\" : [ \"CASSANDRA=%s\", \"MDB_SERVER=%s\", \"MDB_PW=%s\" ], \"Volumes\" : { }, \"ExposedPorts\" : { }, \"HostConfig\" : { \"Binds\" : [ ], \"NetworkMode\" : \"host\" }}" ${CASSANDRA} ${MDB_SERVER} ${PASSWORD}  > container_settings.json
