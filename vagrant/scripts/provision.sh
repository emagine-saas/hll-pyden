#!/usr/bin/env bash

set -x

curl -o /tmp/splunk.rpm 'https://download.splunk.com/products/splunk/releases/8.0.1/linux/splunk-8.0.1-6db836e2fb9e-linux-2.6-x86_64.rpm' 
# 'https://www.splunk.com/bin/splunk/DownloadActivityServlet?architecture=x86_64&platform=linux&version=7.3.2&product=splunk&filename=splunk-8.0.1-6db836e2fb9e-linux-2.6-x86_64.rpm&wget=true'
if [ "$?" = "0" ] ; then
sudo yum -y install /tmp/splunk.rpm
fi

sudo timedatectl set-timezone Europe/London
sudo cp /home/vagrant/.bashrc ${SPLUNK_HOME}/.bashrc
sudo chown splunk:splunk ${SPLUNK_HOME}/.bashrc
sudo cp /home/vagrant/.profile ${SPLUNK_HOME}/.profile
sudo chown splunk:splunk ${SPLUNK_HOME}/.bashrc
echo "alias splunk=${SPLUNK_BIN}" | sudo tee -a ${SPLUNK_HOME}/.bashrc > /dev/null
echo "splunk:${SPLUNK_PASS}" | sudo chpasswd
sudo yum -y group install "Development Tools"
sudo yum -y install sshpass libffi-dev libssl-dev
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

