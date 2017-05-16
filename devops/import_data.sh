#!/bin/bash

set -v -e

docker-compose up -d dev-with-db

# wait for api to startup
until (curl http://localhost:8001/api/notice &>/dev/null)
do
  echo "Startup: Waiting for API"
  sleep 1
done

cd eregs_extensions
PARSE="docker-compose -f docker-compose.yml -f atf-network.yml run --rm eregs"

$PARSE pipeline 27 447 http://dev-with-db:8001/api
$PARSE pipeline 27 478 http://dev-with-db:8001/api
$PARSE pipeline 27 479 http://dev-with-db:8001/api
$PARSE pipeline 27 555 http://dev-with-db:8001/api
$PARSE pipeline 27 646 http://dev-with-db:8001/api
