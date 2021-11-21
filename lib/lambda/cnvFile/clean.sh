#!/bin/bash
rm -rf ./package
rm -rf ./tmp_for_check_the_docker_deamon_running
rm -rf ./.venv
rm -f ./deployment-package.zip
rm -f ./requirements.txt

CONTAINER_NAME=dind
sh ./docker_sh/rmc.sh $CONTAINER_NAME
sh ./docker_sh/rmi.sh $CONTAINER_NAME
