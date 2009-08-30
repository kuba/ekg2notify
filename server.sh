#!/bin/bash
# server.sh

PORT=1025
PASS='test'

cat notify | while true;
             do
                 cryptcat -k $PASS -l -p $PORT
             done
