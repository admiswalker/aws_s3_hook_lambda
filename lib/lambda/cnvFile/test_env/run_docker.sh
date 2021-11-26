#!/bin/bash
CONTAINER_NAME=test-lambda
IMAGE_NAME=test-lambda
docker run --rm -it --name $CONTAINER_NAME -v /var/run/docker.sock:/var/run/docker.sock -v $PWD:/home -w /home $IMAGE_NAME test/test
