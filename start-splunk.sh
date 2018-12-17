#!/usr/bin/env bash

status=`sudo -u splunk ${SPLUNK_BIN} status`

#echo "Splunk status is: $status"

# maybe status command can emit status codes instead...
if [ "$status" != *"not running"* ]; then
    echo Splunk was not running
    sudo -u splunk ${SPLUNK_BIN} start
else
    echo Splunk is running
fi
IP=$(ifconfig eth1 | sed -ne 's/.*inet \([0-9.]\+\) .*/\1/p')
cowsay <<MOO
        Splunk is available: "${IP}:8000"
MOO