#!/bin/bash
docker run --rm -it --name aws-lambda-python-3.8 -v $PWD:/home -w /home amazon/aws-lambda-python:3.8.2021.11.08.18 sh
