#!/usr/bin/env bash

DOCKER_IMAGE_NAME="algox"
echo "Building the Jupyter notebook docker image ('${DOCKER_IMAGE_NAME}') with a PyPy kernel..."
docker build -t ${DOCKER_IMAGE_NAME} .