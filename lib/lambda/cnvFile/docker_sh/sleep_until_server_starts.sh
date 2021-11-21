#!/bin/bash

# Usage:
#   DinD_CONTAINER_NAME=xxx
#   ./docker_sh/sleep_until_server_starts.sh $DinD_CONTAINER_NAME

echo 'waiting docker daemon...'

IMAGE_NAME=$1
CONTAINER_NAME=$2
echo $IMAGE_NAME
echo $CONTAINER_NAME

while :
do
    #CONTAINER_ID=$(docker ps | grep $CONTAINER_NAME | awk '{print $1}')
    #str_len=${#CONTAINER_ID}
    #echo $str_len
    #if [ ${str_len} != 0 ]; then
    #   break
    #fi
    #echo 'waiting docker daemon...'
    #sleep 1

    str=$(docker exec -it $CONTAINER_NAME docker pull $IMAGE_NAME)
    echo '$str'
    echo $str
    str_len=${#str}
    echo '$str_len'
    echo $str_len
    if [ $str_len == 0 ]; then
	echo 'waiting docker daemon...'
	echo 'in 01'
	sleep 1
    elif [[ $str =~ 'not connect to the Docker daemon' ]]; then
	echo 'waiting docker daemon...'
	echo 'in 02'
	sleep 1
    else
	echo 'in 03'
        exit
    fi
done


#    if docker info > /dev/null 2>&1; then
#        break
#    fi

