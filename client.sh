#!/bin/bash

CRYPTCAT_PASSWORD='test'
CRYPTCAT_HOST='s'
CRYPTCAT_PORT=1234

usage="USAGE:\n\t`basename $0` ssh <standard arguments apply>\n\t`basename $0` cryptcat"

process_pipe() {
    tee /dev/stderr | while IFS=$'\t\r' read -a args; do notify-send "${args[@]}"; done
}

case $1 in
    ssh)
    "$@" -t cat notify | process_pipe;
    ;;
    cryptcat)
    if cryptcat -k $CRYPTCAT_PASSWORD $CRYPTCAT_HOST $CRYPTCAT_PORT | process_pipe;
    then
        echo "Is cryptcat-server.sh running?";
    fi
    ;;
    *)
    echo -e $usage;
    ;;
esac
