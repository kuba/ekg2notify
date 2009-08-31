#!/bin/bash

PORT=1234
PASSWORD='test'

cat notify | while true;
             do
                 cryptcat -k $PASSWORD -l -p $PORT
             done
