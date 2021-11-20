#!/bin/bash

# Usage:
#   CONTAINER_NAME=xxx
#   ./docker_rm.sh $CONTAINER_NAME

CONTAINER_NAME=$1
IMAGE_ID_str=$(docker inspect --format="{{.Id}}" $CONTAINER_NAME) # sha256:80a2138b2d88c11a2e556b162d6a42d720aeabc9bc512122b66d6edc86d05037
IMAGE_ID_arr=(`echo $IMAGE_ID_str | tr -s ':' ' '`)               # [sha256, 80a2138b2d88c11a2e556b162d6a42d720aeabc9bc512122b66d6edc86d05037]
IMAGE_ID=${IMAGE_ID_arr[1]}                                       # 80a2138b2d88c11a2e556b162d6a42d720aeabc9bc512122b66d6edc86d05037
docker rmi $IMAGE_ID
