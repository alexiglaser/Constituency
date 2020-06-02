#!/usr/bin/env bash

DOCKER_IMAGE_NAME="algox-analysis"
echo "Running the pypi-Jupyter notebook docker image '${DOCKER_IMAGE_NAME}'..."
docker run -it -p 8888:8888            \
               -v "$PWD"/..:/home/work \
               "${DOCKER_IMAGE_NAME}" /bin/bash