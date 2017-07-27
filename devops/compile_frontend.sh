#!/bin/bash

set -e

if [ -z "$1" ]; then
  echo "Needs a parameter: build-dist or build-dev"
  exit
fi

# We don't want to use --clear as we don't want to delete node_modules
rm -rf frontend_build/config frontend_build/regulations
mkdir -p compiled
rm -rf compiled/regulations
docker-compose run --rm manage.py collectstatic --no-default-ignore --noinput > /dev/null
# Copy config values
cp frontend_build/config/.babelrc frontend_build/
cp frontend_build/config/Gruntfile.js frontend_build/
cp frontend_build/config/package.json frontend_build/
# Build
docker-compose run --rm grunt $1
cp -r frontend_build/regulations compiled/regulations
