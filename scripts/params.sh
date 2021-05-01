#!/bin/bash

PARAM_FIELDS="option name entries default help"

ROOT_PATH="."
if [ -x "$(command -v realpath)" ]; then
  ROOT_PATH=$(realpath "$(dirname "$PRG")")
fi

while read $PARAM_FIELDS; do
  eval "$name=$default"
done < $ROOT_PATH/params.txt


while read; do
  while read $PARAM_FIELDS; do
    if [[ $# -gt 2 ]]; then
      if [[ "$1" == "$option" ]]; then
        eval "$name=$2"
        shift 2
      fi
    fi
  done < $ROOT_PATH/params.txt
done < $ROOT_PATH/params.txt


function echo_help {
  echo "$(basename "$0") -- program to deal with $APP_NAME ecosystem
where:
  -h                                                                                                show this help text"
  while read $PARAM_FIELDS; do
    printf "  %s=%-12s %-50s %-30s %s\n" $option "<$name>" "$(sed -e 's/^"//' -e 's/"$//' <<<"$entries")" "(default: $default)" "$(sed -e 's/^"//' -e 's/"$//' <<<"$help")"
  done < $ROOT_PATH/params.txt
  exit 0
}
