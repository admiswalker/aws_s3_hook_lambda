#!/bin/bash
# CONTAINER_NAME=amazon/aws-lambda-python:3.8.2021.11.08.18
# docker run --rm -it --name $CONTAINER_NAME -v $PWD:/home -w /home $CONTAINER_NAME:latest ./test.sh
# docker run --rm -it --name run_test -v $PWD:/home -w /home amazon/aws-lambda-python:3.8.2021.11.08.18 ./test.sh


pip install poetry
yum install -y zip

cd /home; python3 test.py
