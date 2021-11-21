#!/bin/bash
IMAGE_NAME=docker:19.03.0-dind
CONTAINER_NAME=dind

docker run --rm -it --name $CONTAINER_NAME -v /var/run/docker.sock:/var/run/docker.sock -v $PWD:/home -w /home $IMAGE_NAME sh build_dockerfile.sh
