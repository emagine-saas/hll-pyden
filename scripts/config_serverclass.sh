#!/usr/bin/env bash

sudo -u splunk tee -a ${SPLUNK_HOME}/etc/system/local/serverclass.conf << 'EOF'
[serverClass:forwarders:app:pyden]
restartSplunkWeb = 0
restartSplunkd = 0
stateOnClient = enabled

[serverClass:forwarders]
whitelist.0 = splunk-forwarder
EOF
sudo -u splunk ${SPLUNK_BIN} restart