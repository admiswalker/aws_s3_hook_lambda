#!/bin/bash
docker run --rm -it --name dind -v /var/run/docker.sock:/var/run/docker.sock -v $PWD:/home -w /home docker:stable-dind sh build_dockerfile.sh
