#!/bin/bash

set -e

API="https://api.fr.cloud.gov"
ORG="atf-eregs"
SPACE=$1

MANIFEST="manifest_$SPACE.yml"
if [ ! -f $MANIFEST ]; then
  echo "Unknown space: $SPACE"
  exit
fi

if [ -n "$CF_USERNAME" ] && [ -n "$CF_PASSWORD" ]; then
  cf login -a $API -u $CF_USERNAME -p $CF_PASSWORD
fi
cf target -o $ORG -s $SPACE

cf scale -i 1 atf-eregs
cf zero-downtime-push atf-eregs -f $MANIFEST
cf zero-downtime-push atf-resources-worker -f $MANIFEST
cf zero-downtime-push redeployer -f $MANIFEST
