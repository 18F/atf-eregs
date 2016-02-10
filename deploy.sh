set -e
set -x

API="https://api.cloud.gov"
ORG="eregs"
SPACE=$1

if [ $# -ne 1 ]; then
  echo "Usage: deploy <space>"
  exit
fi

if [ $SPACE = 'prod' ]; then
  NAME="atf-eregs"
  MANIFEST="manifest_prod.yml"
elif [ $SPACE = 'dev' ]; then
  NAME="atf-site"
  MANIFEST="manifest_dev.yml"
else
  echo "Unknown space: $SPACE"
  exit
fi

cf login --a $API --u $CF_USERNAME --p $CF_PASSWORD --o $ORG -s $SPACE
cf zero-downtime-push $NAME -f $MANIFEST
