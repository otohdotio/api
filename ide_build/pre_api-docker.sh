#!/usr/bin/env bash

# Ensure the docker VM is running (Mac OS X)
if [ "$(docker-machine status default)" != "Running" ]; then
    docker-machine start default
fi
eval "$(docker-machine env default)"

# Create an SSH tunnel on 443 to the docker-machine
ps -ef | grep -v grep |  grep 443:localhost:443
if [ "$?" != "0" ]; then
    sudo ssh -f -T -N -L443:localhost:443 -l docker \
      -i ~/.docker/machine/machines/default/id_rsa \
      $(echo $DOCKER_HOST | cut -d ':' -f 2 | tr -d '/')
fi

# Kill and remove any existing api containers
# Note the -I argument to xargs is for Mac OS X compatibility
docker ps | grep api | awk '{print $1}' | xargs -I {} docker kill {}
docker ps -a | grep api | awk '{print $1}' | xargs -I {} docker rm {}

printf "{ \"AttachStdin\" : false, \"Env\" : [ \"CASSANDRA=%s\" ], \"Volumes\" : { }, \"ExposedPorts\" : { }, \"HostConfig\" : { \"Binds\" : [ ], \"NetworkMode\" : \"host\" }}" `docker inspect --format "{{ .NetworkSettings.IPAddress }}" cs1` > ../container_settings.json
