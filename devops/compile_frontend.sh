#!/bin/bash
set -e

if [ -z "$1" ]; then
  echo "Needs a parameter: build-dist or build-dev"
  exit 1
fi

docker-compose run --rm dev ./devops/combine_frontend_sources.sh
# Build
docker-compose run --rm grunt $1
docker-compose run --rm dev cp -r frontend_build/regulations compiled/regulations
