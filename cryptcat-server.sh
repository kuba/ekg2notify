#!/bin/bash

usage="USAGE:\n\t`basename $0` <port> <password>"

if [[ ! $# == 2 ]]
then
    echo -e $usage
    exit
fi

PORT=$1
PASS=$2

cat notify | while true;
             do
                 cryptcat -k $PASS -l -p $PORT
             done
