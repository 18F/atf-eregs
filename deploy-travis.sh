set -e
set -x

cd $TRAVIS_BUILD_DIR
./deploy.sh dev
