#!/usr/bin/env bash

sudo -i -u splunk ${SPLUNK_BIN} bootstrap shcluster-captain -servers_list "https://splunk-search-1:8089,https://splunk-search-2:8089,https://splunk-search-3:8089" -auth admin:${SPLUNK_PASS}
