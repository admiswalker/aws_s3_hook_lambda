#!/bin/bash
CONTAINER_NAME=test-lambda
sh ./docker_sh/rmc.sh $CONTAINER_NAME
sh ./docker_sh/rmi.sh $CONTAINER_NAME
