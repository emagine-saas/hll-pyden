# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

#------------------------------------------------------------------------------
# Configuration you may want to modify
#------------------------------------------------------------------------------
VM_NAME = "splunk-sandbox"
VM_MEMORY = 2048
VM_CPUS = 2
# this is the password you will set for your splunk admin user
SPLUNK_PASS  = "changeme"
# Splunk home directory
SPLUNK_HOME  = "/opt/splunk"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "badarsebard/ubuntu-18.04-splunk"
  config.vm.box_version = "7.2.3.0"
  config.vm.define "#{VM_NAME}"
  config.vm.network "private_network", ip: "192.168.33.10"
  config.vm.hostname = "splunk"
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  # You can use public_network, if you prefer:
  # config.vm.network "public_network", bridge: 'en0: Ethernet'
  
  config.vm.provider "vmware_desktop" do |v|
    v.memory = "#{VM_MEMORY}"
    v.cpus = "#{VM_CPUS}"
  config.vm.synced_folder "src/pyden", "/opt/splunk/etc/apps/pyden",
    owner: "splunk", group: "splunk"
  config.vm.synced_folder "src/pyden-manager", "/opt/splunk/etc/apps/pyden-manager",
    owner: "splunk", group: "splunk"
  config.vm.synced_folder "test-app", "/opt/splunk/etc/apps/test-app",
    owner: "splunk", group: "splunk"
  end

  config.vm.provider "virtualbox" do |v|
    v.memory = "#{VM_MEMORY}"
    v.cpus = "#{VM_CPUS}"
  config.vm.synced_folder "src/pyden", "/opt/splunk/etc/apps/pyden",
    owner: "splunk", group: "splunk"
  config.vm.synced_folder "src/pyden-manager", "/opt/splunk/etc/apps/pyden-manager",
    owner: "splunk", group: "splunk"
  config.vm.synced_folder "test-app", "/opt/splunk/etc/apps/test-app",
    owner: "splunk", group: "splunk"
  end

  config.vm.provision "bootstrap", type: "shell" do |s|
    s.privileged = false
    s.name ="Bootstrap Provisioner"
    s.path = "provision.sh"
    s.env = {
      :SPLUNK_HOME  => "#{SPLUNK_HOME}",
      :SPLUNK_BIN   => "#{SPLUNK_HOME}/bin/splunk",
      :SPLUNK_PASS  => "#{SPLUNK_PASS}"
    }
  end

  config.vm.provision "startup", type: "shell", run: "always" do |t|
    t.privileged = false
    t.name ="Start up provisioner"
    t.path = "start-splunk.sh"
    t.env = { :SPLUNK_BIN   => "/opt/splunk/bin/splunk" }
  end
end
