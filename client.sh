#/bin/bash
# client.sh

HOST='s'
PORT=1025
PASS='test'

cryptcat -k $PASS $HOST $PORT  | sed -u -e "s/'/'\\\\''/g" | sed -u -e "s/\(.*\)\t\(.*\)/notify-send '\1' '\2' -i notification-message-im/" | bash
