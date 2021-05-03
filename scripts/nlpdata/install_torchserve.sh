#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
set -o allexport
source $BASEDIR/../../.env
set +o allexport

echo "### Set admin user password..."
read -s -p "torchserve's admin password: " TORCHSERVE_ADMIN_PASSWORD
echo

echo "### Starting geoserver..."
export TORCHSERVE_ADMIN_PASSWORD=$TORCHSERVE_ADMIN_PASSWORD && docker-compose -f docker-compose.serve-ovh.yml up --force-recreate -d torchserve-serve-ovh
