set -e
set -x

cd $TRAVIS_BUILD_DIR

# Install cf cli
export PATH=.:$PATH
curl -L -o cf.tgz "https://cli.run.pivotal.io/stable?release=linux64-binary&version=6.15.0"
tar xzvf cf.tgz

# Install autopilot
mkdir -p ${TRAVIS_BUILD_DIR}/Godeps/_workspace
export GOPATH=${TRAVIS_BUILD_DIR}/Godeps/_workspace
go get github.com/concourse/autopilot
cf install-plugin -f $GOPATH/bin/autopilot

./deploy.sh dev
