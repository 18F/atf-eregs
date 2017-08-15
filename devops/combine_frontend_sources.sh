#!/bin/bash
# Steps that combine frontend code from -site and atf in preparation for compilation
# This should be ran inside one of the Python containers
set -e
shopt -s dotglob

# We don't want to use --clear as we don't want to delete node_modules
rm -rf frontend_build/config frontend_build/regulations
rm -rf compiled/regulations
./devops/activate_then ./manage.py collectstatic --no-default-ignore --noinput > /dev/null
# Copy config values
cp frontend_build/config/* frontend_build/
