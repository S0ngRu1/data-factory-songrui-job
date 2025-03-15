#!/bin/bash

IMAGE=""
CONTAINER="-server"

set -x
NAME="$CONTAINER"
docker ps | awk '{print $NF}' | grep -E "^$NAME$"
if [ $? -eq 0 ]; then
    docker kill $NAME
fi
docker ps -a | awk '{print $NF}' | grep -E "^$NAME$"
if [ $? -eq 0 ]; then
  docker rm $NAME
fi

docker run --name "$NAME" -d -p 18881:8082 --restart unless-stopped -v /etc/localtime:/etc/localtime:ro "$IMAGE:latest"