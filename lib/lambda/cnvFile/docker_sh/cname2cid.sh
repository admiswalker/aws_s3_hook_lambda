#!/bin/bash

# Usage:
#   CONTAINER_NAME=xxx
#   CONTAINER_ID=./docker_sh/cname2cid.sh $CONTAINER_NAME

CONTAINER_NAME=$1
CONTAINER_ID=$(docker ps | grep $CONTAINER_NAME | awk '{print $1}')
echo $CONTAINER_ID
