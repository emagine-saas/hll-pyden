#!/usr/bin/env bash

sudo -i -u splunk ${SPLUNK_BIN} add search-server https://splunk-indexer:8089 -auth admin:${SPLUNK_PASS} -remoteUsername admin -remotePassword ${SPLUNK_PASS}
