#!/bin/bash

BASEDIR=$(dirname "$0")
set -o allexport
source $BASEDIR/../../.env
set +o allexport

if ! [ -x "$(command -v docker-compose)" ]; then
  echo 'Error: docker-compose is not installed.' >&2
  exit 1
fi

SERVER_NAME=${DATA_SUBDOMAIN}.${APP_NAME}.${TLD}
DOMAINS=($SERVER_NAME)
DATA_PATH="./docker_data_serve-ovh/certbot"
EMAIL="infra@$APP_NAME.$TLD"
RSA_KEY_SIZE=4096
TESTING_SETUP=0 # Set to 1 if you're testing your setup to avoid hitting request limits

if [ -d "$DATA_PATH" ]; then
  read -p "Existing data found for $DOMAINS. Continue and replace existing certificate? (y/N) " DECISION
  if [ "$DECISION" != "Y" ] && [ "$DECISION" != "y" ]; then
    exit
  fi
fi


if [ ! -e "$DATA_PATH/conf/options-ssl-nginx.conf" ] || [ ! -e "$DATA_PATH/conf/ssl-dhparams.pem" ]; then
  echo "### Downloading recommended TLS parameters ..."
  mkdir -p "$DATA_PATH/conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf > "$DATA_PATH/conf/options-ssl-nginx.conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem > "$DATA_PATH/conf/ssl-dhparams.pem"
  echo
fi

echo "### Creating dummy certificate for $DOMAINS..."
LIVE_PATH="/etc/letsencrypt/live/$DOMAINS"
mkdir -p "$DATA_PATH/conf/live/$DOMAINS"
docker-compose -f docker-compose.serve-ovh.yml run --rm --entrypoint "\
  openssl req -x509 -nodes -newkey rsa:1024 -days 1\
    -keyout '$LIVE_PATH/privkey.pem' \
    -out '$LIVE_PATH/fullchain.pem' \
    -subj '/CN=localhost'" certbot-serve-ovh
echo


echo "### Starting nginx..."
docker-compose -f docker-compose.serve-ovh.yml build --no-cache nginx-serve-ovh
docker-compose -f docker-compose.serve-ovh.yml up --force-recreate -d nginx-serve-ovh
echo

echo "### Deleting dummy certificate for $DOMAINS..."
docker-compose -f docker-compose.serve-ovh.yml run --rm --entrypoint "\
  rm -Rf /etc/letsencrypt/live/$DOMAINS && \
  rm -Rf /etc/letsencrypt/archive/$DOMAINS && \
  rm -Rf /etc/letsencrypt/renewal/$DOMAINS.conf" certbot-serve-ovh
echo


echo "### Requesting Let's Encrypt certificate for $DOMAINS..."
#Join $DOMAINS to -d args
DOMAIN_ARGS=""
for DOMAIN in "${DOMAINS[@]}"; do
  DOMAIN_ARGS="$DOMAIN_ARGS -d $DOMAIN"
done

# Select appropriate EMAIL arg
case "$EMAIL" in
  "") EMAIL_ARG="--register-unsafely-without-email" ;;
  *) EMAIL_ARG="--email $EMAIL" ;;
esac

# Enable TESTING_SETUP mode if needed
if [ $TESTING_SETUP != "0" ]; then TESTING_SETUP_ARG="--staging"; fi

docker-compose -f docker-compose.serve-ovh.yml run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
    $TESTING_SETUP_ARG \
    $EMAIL_ARG \
    $DOMAIN_ARGS \
    --rsa-key-size $RSA_KEY_SIZE \
    --agree-tos \
    --force-renewal" certbot-serve-ovh
echo

echo "### Reloading nginx..."
chgrp 101 -R $DATA_PATH/*
chmod g+rx -R $DATA_PATH/*
docker exec `docker ps | grep nginx-serve-ovh | cut -d" " -f 1` nginx -s reload
