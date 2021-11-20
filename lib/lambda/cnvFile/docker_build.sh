#!/bin/bash
CONTAINER_NAME=gen-deployment-package
GEN_TARGET=deployment-package.zip

docker build -t $CONTAINER_NAME ./
./docker_cp.sh $CONTAINER_NAME ./home/$GEN_TARGET .

IMAGE_ID=$(docker inspect --format="{{.Id}}" $CONTAINER_NAME)

