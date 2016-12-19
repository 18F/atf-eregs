set -e

API="https://api.fr.cloud.gov"
ORG="atf-eregs"
SPACE=$1

if [ $# -ne 1 ]; then
  echo "Usage: deploy <space>"
  exit
fi

NAME="atf-eregs"

if [ $SPACE = 'prod' ]; then
  MANIFEST="manifest_prod.yml"
elif [ $SPACE = 'dev' ]; then
  MANIFEST="manifest_dev.yml"
else
  echo "Unknown space: $SPACE"
  exit
fi

cf login --a $API --u $CF_USERNAME --p $CF_PASSWORD --o $ORG -s $SPACE
cf zero-downtime-push $NAME -f $MANIFEST
