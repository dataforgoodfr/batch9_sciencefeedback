#!/bin/bash

MINIMAL_DOCKER_VERSION=${MINIMAL_DOCKER_VERSION-''}
if [ ! -z $MINIMAL_DOCKER_VERSION ]; then
  CURRENT_DOCKER_VERSION=$(docker -v | cut -d',' -f1 | cut -d' ' -f3)
  version_is_less $CURRENT_DOCKER_VERSION $MINIMAL_DOCKER_VERSION && exit_with_error 'You need a docker version >='$MINIMAL_DOCKER_VERSION
fi

MINIMAL_DOCKER_COMPOSE_VERSION=${MINIMAL_DOCKER_COMPOSE_VERSION-''}
if [ ! -z $MINIMAL_DOCKER_COMPOSE_VERSION ]; then
  CURRENT_DOCKER_COMPOSE_VERSION=$(docker-compose -v | cut -d',' -f1 | cut -d' ' -f3)
  version_is_less $CURRENT_DOCKER_COMPOSE_VERSION $MINIMAL_DOCKER_COMPOSE_VERSION && exit_with_error 'You need a docker-compose version >='$MINIMAL_DOCKER_COMPOSE_VERSION
fi

MINIMAL_YARN_VERSION=${MINIMAL_YARN_VERSION-''}
if [ ! -z $MINIMAL_YARN_VERSION ]; then
  CURRENT_YARN_VERSION=$(yarn -v)
  version_is_less $CURRENT_YARN_VERSION $MINIMAL_YARN_VERSION && exit_with_error 'You need a yarn version >='$MINIMAL_YARN_VERSION
fi

if [[ "$TAG" != "not-set" ]] && [[ ! "$TAG" =~ ^[0-9]+\.[0-9]+\.[0-9]+ ]]; then
  exit_with_error "-t tag option : tag format should be semantic versioning compliant x.x.x"
fi

if [[ ! -f $ROOT_PATH/.env ]]; then
  exit_with_error "There is no .env file, you need to ask for one !"
fi
