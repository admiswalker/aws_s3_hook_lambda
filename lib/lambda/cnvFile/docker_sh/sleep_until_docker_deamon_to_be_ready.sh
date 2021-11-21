#!/bin/bash

# Usage:
#   CONTAINER_NAME=xxx
#   ./docker_sh/sleep_until_server_starts.sh $CONTAINER_NAME

CONTAINER_NAME=$1

while :
do
    echo 'waiting for docker daemon to be ready...'

    str=$(docker exec -it $CONTAINER_NAME docker build ./docker_sh/for_check_the_docker_deamon_running)
    str_len=${#str}
    if [ $str_len == 0 ]; then
	sleep 1
    elif [[ $str =~ 'not connect to the Docker daemon' ]]; then
	sleep 1
    else
        exit 0
    fi
done
