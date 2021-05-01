#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
set -o allexport
source $BASEDIR/../../.env
set +o allexport

echo "### Install linux dependencies curl, git..."
apt-get update
apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        git \
        gnupg2 \
        python-openstackclient \
        python-novaclient \
        software-properties-common
echo

echo "### Install docker ..."
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
apt-key fingerprint 0EBFCD8
add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable"
apt-get update
apt-get install -y \
        docker-ce \
        docker-ce-cli \
        containerd.io
usermod -a -G docker $NLPDATA_USER
newgrp docker
docker run hello-world

echo

echo "### Install docker compose..."
DOCKER_COMPOSE_VERSION=1.23.2
rm -f /usr/local/bin/docker-compose
curl -L "https://github.com/docker/compose/releases/download/$DOCKER_COMPOSE_VERSION/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
sleep 1
echo
