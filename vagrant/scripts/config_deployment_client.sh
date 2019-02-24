#!/usr/bin/env bash

sudo -i -u splunk ${SPLUNK_BIN} set deploy-poll splunk-server:8089 -auth admin:${SPLUNK_PASS}
sudo -i -u splunk ${SPLUNK_BIN} restart