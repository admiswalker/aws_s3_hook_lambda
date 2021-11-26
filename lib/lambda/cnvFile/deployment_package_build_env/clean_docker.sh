#!/bin/bash
CONTAINER_NAME=dind
sh ./docker_sh/rmc.sh $CONTAINER_NAME
sh ./docker_sh/rmi.sh $CONTAINER_NAME
