#!/usr/bin/env bash

BASEDIR=$(dirname "$0")


set -o allexport
source $BASEDIR/quit_screen_sessions.sh
source $BASEDIR/../../.env
set +o allexport

docker-compose -f docker-compose.serve-ovh.yml build --no-cache certbot-serve-ovh torchserve-serve-ovh nginx-serve-ovh
docker stop $APP_NAME-certbot-serve-ovh $APP_NAME-torchserve-serve-ovh $APP_NAME-nginx-serve-ovh || true
quit_screen_sessions nlpdata
screen -S nlpdata -dm
COMMAND="
  docker-compose -f docker-compose.serve-ovh.yml up certbot-serve-ovh torchserve-serve-ovh nginx-serve-ovh;
"
screen -r nlpdata -X stuff "$COMMAND\n"
