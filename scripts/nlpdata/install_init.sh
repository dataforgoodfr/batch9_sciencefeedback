#!/usr/bin/env bash

echo "### Install linux dependencies curl, git..."
apt-get update
apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        git \
        gnupg2 \
        software-properties-common
echo
