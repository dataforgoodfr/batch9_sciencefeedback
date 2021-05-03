#!/usr/bin/env bash

function quit_screen_sessions {
  SESSION_NAME="$1"

  SESSION_IDS=$(screen -ls $SESSION_NAME | grep $SESSION_NAME | cut -d"." -f1 | sed ':a;N;$!ba;s/\n//g')
  for SESSION_ID in $SESSION_IDS
  do
    screen -S $SESSION_ID -X quit
  done
}
