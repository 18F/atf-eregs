set -e

cd $TRAVIS_BUILD_DIR
export PATH=$TRAVIS_BUILD_DIR:$PATH
./deploy.sh dev
