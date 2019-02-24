#!/usr/bin/env bash

sudo -i -u splunk  ${SPLUNK_BIN} init shcluster-config -auth admin:${SPLUNK_PASS} -mgmt_uri https://${MGMT_URI} -replication_port 9887 -conf_deploy_fetch_url https://splunk-deployer:8089 -secret ${SPLUNK_PASS} -shcluster_label shcluster

sudo -u splunk ${SPLUNK_BIN} restart