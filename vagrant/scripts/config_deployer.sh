#!/usr/bin/env bash

sudo -u splunk tee -a ${SPLUNK_HOME}/etc/system/local/server.conf << EOF
[shclustering]
pass4SymmKey = ${SPLUNK_PASS}
shcluster_label = shcluster
EOF

sudo -i -u splunk ${SPLUNK_BIN} restart