#!/bin/bash

function echo_help {
  echo "$(basename "$0") -- program to deal with $APP_NAME ecosystem
where:
  -h                                                                                                show this help text"
  while read $PARAM_FIELDS; do
    printf "  %s=%-12s %-50s %-30s %s\n" $option "<$name>" "$(sed -e 's/^"//' -e 's/"$//' <<<"$entries")" "(default: $default)" "$(sed -e 's/^"//' -e 's/"$//' <<<"$help")"
  done < $ROOT_PATH/params.txt
  exit 0
}


function check {
  STATE=$1
  CONTAINER=${APP_NAME}-${2}-${COMPOSITION}
  GREP=$(docker ps | grep $CONTAINER)
  if [[ "$GREP" ]]; then
    if [[ "$STATE" == "stop" ]]; then
      exit_with_error "$CONTAINER is running. You should stop it before applying your command."
    fi
  elif [[ "$STATE" == "start" ]]; then
    exit_with_error "$CONTAINER is not running. You should start it before applying your command."
  fi
}


function confirm {
  read -p "$1 (y/n) : " -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit
  fi
}


function containers_from_names {
  FIELDS=("${@/#}")
  FIELDS=("${FIELDS[@]/%/-$COMPOSITION}")
  echo "${FIELDS[*]}"
}


function ensure_development {
  if [[ "$ENV" != "development" ]] & [[ "$ENV" != "not-set" ]]; then
    exit_with_error "${1:-can only be executed in development}."
  fi
}


function ensure_remote {
  if [[ "$ENV" == "not-set" ]] | [[ "$ENV" == "development" ]]; then
    exit_with_error "${1:-can only be executed in remote (like production)}."
  fi
}


function exit_with_error {
  MESSAGE=${1-"end of $APP_NAME command."}
  RED='\033[0;31m'
  NO_COLOR='\033[0m'
  echo -e "${RED}""ERROR : $MESSAGE""${NO_COLOR}"
  exit 1
}


function exit_with_success {
  if [ $LOG == "on" ]; then
    MESSAGE=${1-"end of $APP_NAME command."}
    GREEN='\033[0;32m'
    NO_COLOR='\033[0m'
    echo -e "${GREEN}""SUCCESS : $MESSAGE""${NO_COLOR}"
  fi
  exit 0
}


function update_branch {
  branch="$1"
  git fetch
  git checkout $branch
  git reset --hard origin/$branch || (git checkout "$CURRENT_BRANCH" && exit_with_error)
}



version_is_less_or_equal() {
  [ "$1" = "`echo -e "$1\n$2" | sort -V | head -n1`" ]
}


version_is_less() {
  [ "$1" = "$2" ] && return 1 || version_is_less_or_equal $1 $2
}
