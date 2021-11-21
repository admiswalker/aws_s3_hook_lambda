#!/bin/bash
IMAGE_NAME=docker:19.03.0-dind
CONTAINER_NAME=dind

docker run --privileged -d --name $CONTAINER_NAME -v $PWD:/home -w /home $IMAGE_NAME &
./docker_sh/sleep_until_docker_deamon_to_be_ready.sh $CONTAINER_NAME

CONTAINER_ID=$(docker ps | grep $CONTAINER_NAME | awk '{print $1}')
docker exec -it $CONTAINER_NAME sh ./build_dockerfile.sh

docker stop $CONTAINER_ID
docker rm $CONTAINER_ID
