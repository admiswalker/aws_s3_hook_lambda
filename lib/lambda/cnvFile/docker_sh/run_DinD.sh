#!/bin/bash

# Usage:
#   DinD_CONTAINER_NAME=xxx
#   ./docker_sh/run_DinD.sh $DinD_CONTAINER_NAME

DinD_CONTAINER_NAME=$1
docker run --privileged -d --name dind -v $PWD:/home -w /home $DinD_CONTAINER_NAME

