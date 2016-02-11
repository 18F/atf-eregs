set -e

cd $TRAVIS_BUILD_DIR
export PATH=$TRAVIS_BUILD_DIR:$PATH

echo $TRAVIS_BUILD_DIR
echo $CF_USERNAME
pwd
ls -lah

./deploy.sh dev
