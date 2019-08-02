#!/usr/bin/env bash

sudo timedatectl set-timezone America/New_York
sudo -u splunk cp /home/vagrant/.bashrc ${SPLUNK_HOME}/.bashrc
sudo -u splunk cp /home/vagrant/.profile ${SPLUNK_HOME}/.profile
echo "alias splunk=${SPLUNK_BIN}" | sudo tee -a ${SPLUNK_HOME}/.bashrc > /dev/null
echo "splunk:${SPLUNK_PASS}" | sudo chpasswd
sudo DEBIAN_FRONTEND=noninteractive apt-get update -yq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -yq sshpass build-essential libffi-dev libssl-dev
# sudo apt-get install -yq sshpass build-essential libncurses5-dev libgdbm-dev libdb5.3-dev libbz2-dev liblzma-dev libsqlite3-dev libffi-dev tcl-dev tk tk-dev libdb-dev libexpat-dev libpcap-dev libpcre3-dev
cat << EOF | sudo -u splunk tee -a ${SPLUNK_HOME}/etc/system/local/user-seed.conf
[user_info]
USERNAME = admin
PASSWORD = ${SPLUNK_PASS}
EOF
sudo -u splunk tee -a ${SPLUNK_HOME}/etc/log-local.cfg << 'EOF'
[python]
splunk.pyden = DEBUG
EOF
sudo -u splunk tee -a ${SPLUNK_HOME}/bin/python_splunk.sh << 'EOF'
#!/bin/bash
"$(dirname "$0")/splunk" cmd python "$@"
EOF
sudo -u splunk chmod +x ${SPLUNK_HOME}/bin/python_splunk.sh
sudo -u splunk touch ${SPLUNK_HOME}/etc/.ui_login
sudo -i -u splunk ${SPLUNK_BIN} start --accept-license --no-prompt
