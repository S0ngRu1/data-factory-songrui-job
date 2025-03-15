#!/bin/bash
set -x
BASE_DIR=`dirname $(dirname $0)`
echo "base:$BASE_DIR"
NAME=""

CONTAINER="zhurong-server"
docker ps | awk '{print $NF}' | grep -E "^$CONTAINER$"
if [ $? -eq 0 ]; then
    docker kill $CONTAINER
fi

docker images | awk '{print $1}' | grep -E "^$NAME$"
if [ $? -eq 0 ]; then
  docker rmi -f $NAME
fi
docker build . -t $NAME