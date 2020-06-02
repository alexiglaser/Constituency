#!/usr/bin/env bash

DOCKER_IMAGE_NAME="algox-analysis"
echo "Building the pypi-Jupyter notebook docker image '${DOCKER_IMAGE_NAME}'..."
docker build -t ${DOCKER_IMAGE_NAME} .