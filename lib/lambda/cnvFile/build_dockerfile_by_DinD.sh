#!/bin/bash
DinD_IMAGE_NAME=docker:19.03.0-dind
DinD_CONTAINER_NAME=dind
#(docker run --privileged -d --name dind -v $PWD:/home -w /home $DinD_CONTAINER_NAME) & \
#    (DinD_CONTAINER_ID=$(docker ps | grep $DinD_CONTAINER_NAME | awk '{print $1}')) & \
#    (sleep 1); (docker exec -it dind sh ./build_dockerfile.sh)

#docker run --privileged --name $DinD_CONTAINER_NAME -v $PWD:/home -w /home $DinD_IMAGE_NAME sh ./docker_sh/sleep_until_server_starts.sh &
docker run --privileged -d --name $DinD_CONTAINER_NAME -v $PWD:/home -w /home $DinD_IMAGE_NAME &
#docker run --privileged -d --name $DinD_CONTAINER_NAME -v $PWD:/home -w /home $DinD_IMAGE_NAME sh ./docker_sh/sleep_until_server_starts.sh
#docker run --privileged -d --name $DinD_CONTAINER_NAME -v $PWD:/home -w /home $DinD_IMAGE_NAME ./docker_sh/sleep_until_server_starts.sh
#sh ./docker_sh/run_DinD.sh $DinD_CONTAINER_NAME

#sleep 10
./docker_sh/sleep_until_server_starts.sh $DinD_IMAGE_NAME $DinD_CONTAINER_NAME

echo '-----02'
DinD_CONTAINER_ID=$(docker ps | grep $DinD_CONTAINER_NAME | awk '{print $1}')
echo '-----03'
docker exec -it $DinD_CONTAINER_NAME sh ./build_dockerfile.sh

echo '-----04'
docker stop $DinD_CONTAINER_ID
docker rm $DinD_CONTAINER_ID
