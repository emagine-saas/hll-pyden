#!/usr/bin/env bash

sudo -u splunk cp /home/vagrant/.bashrc /opt/splunk/.bashrc
sudo -u splunk cp /home/vagrant/.profile /opt/splunk/.profile
echo 'alias splunk=/opt/splunk/bin/splunk' | sudo tee -a /opt/splunk/.bashrc > /dev/null
sudo DEBIAN_FRONTEND=noninteractive apt-get update -yq
sudo DEBIAN_FRONTEND=noninteractive apt-get upgrade -yq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -yq cowsay build-essential openssl libssl-dev zlib1g-dev libncurses5-dev libreadline-dev libgdbm-dev libdb5.3-dev libbz2-dev liblzma-dev libsqlite3-dev libffi-dev tcl-dev tk tk-dev libdb-dev libexpat-dev libpcap-dev libpcre3-dev
sudo -u splunk tee -a /opt/splunk/etc/system/local/user-seed.conf << 'EOF'
[user_info]
USERNAME = admin
PASSWORD = changeme
EOF
sudo -u splunk tee -a /opt/splunk/etc/log-local.cfg << 'EOF'
[python]
splunk.pyden = DEBUG
EOF

sudo -i -u splunk ${SPLUNK_BIN} start --accept-license --no-prompt
