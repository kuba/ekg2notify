#!/bin/bash

usage="USAGE:\n\t`basename $0` ssh <standard arguments apply>\n\t`basename $0` cryptcat <host> <port> <password>"

if [[ $1 == 'ssh' ]]
then
    # Using SSH
    command="$* -t cat notify | sed -u -e 's/\\r//'"
elif [[ $1 == 'cryptcat' && $# == 4 ]]
then
    # Using cryptcat
    command="cryptcat -k $4 $2 $3"
else
    echo -e $usage
    exit
fi

eval $command | sed -u -n -e "s/\r//" -e "s/'/'\\\\''/g" -e "s/^\(.*\)\t\(.*\)$/notify-send '\1' '\2' -i notification-message-im/p" | bash

if [[ $? -eq 0 && $1 == 'cryptcat' ]]
then
    echo "Is cryptcat-server.sh running?"
fi
