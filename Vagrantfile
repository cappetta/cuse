# -*- mode: ruby -*-
# vi: set ft=ruby :

unless Vagrant.has_plugin?("vagrant-docker-compose")
  system("vagrant plugin install vagrant-docker-compose")
  puts "Dependencies installed, please try the command again."
  exit
end

# Logic to determine the Operating System
module OS
    def OS.windows?
        (/cygwin|mswin|mingw|bccwin|wince|emx/ =~ RUBY_PLATFORM) != nil
    end

    def OS.mac?
        (/darwin/ =~ RUBY_PLATFORM) != nil
    end

    def OS.unix?
        !OS.windows?
    end

    def OS.linux?
        OS.unix? and not OS.mac?
    end
end

# If windows do not install the RSYNC plugin
if !OS.windows?
    # puts "Vagrant launched from mac."
    unless Vagrant.has_plugin?("vagrant-gatling-rsync")
      system("vagrant plugin install vagrant-gatling-rsync")
      puts "Rsync Dependency installed, please try the command again."
    end
end

require 'yaml'
nodes = YAML.load_file("./yaml/vagrant.yaml")



Vagrant.configure("2") do |config|


 nodes.each do |node|
  config.vm.define node["name"] do |node_config|
    node_config.vm.box = node["box"]

    node["forwards"].each do |port|
        node_config.vm.network "forwarded_port", guest: port["guest"], host: port["host"], id: port["id"]
    end

    unless node['folders'].nil? 
      node['folders'].each do |folder|
        node_config.vm.synced_folder folder['local'], folder['virtual']
      end
    end

    config.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--cpus", "2", "--memory", "2048"]
      vb.gui = node["gui"]
      vb.customize ["modifyvm", :id, "--memory",  node["ram"] ]
      vb.customize ["modifyvm", :id, "--cpus",  node["cpu"] ]
      vb.customize ["modifyvm", :id, "--vram",    node["vram"]]
      vb.customize ["modifyvm", :id, "--name",    node["name"]]
      vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      # todo: this is a pain in the ass - first you need to uncomment this, run the automation script, then comment this so when it loops all is good.
      # virtualbox errors if the asset isn't available so we need to check if available then create else skip.. ruby logic

      # vb.customize ["storagectl", :id, "--name", "guestAdditions", "--add", "ide"]
      vb.customize [
                 'storageattach', :id,
                 "--storagectl", "guestAdditions",
                 '--port', '1',
                 '--device', "0",
                 '--type', "dvddrive",
                 '--medium', "VBoxGuestAdditions.iso"
      ]
    end
    #config.vbguest.iso_path = 'http://download.virtualbox.org/virtualbox/%{version}/VBoxGuestAdditions_%{version}.iso'
    #config.vbguest.auto_update = true

    config.vm.synced_folder './', '/vagrant'
    #config.vm.provision :shell, inline: "apt-get update"
    unless node["initScript"].nil?
      node["initScript"].each do |script|
        node_config.vm.provision :shell, path: script["init"], privileged: true
      end
    end
  end

   # # Run Puppet Manifests to setup virtual Desktop env
   # config.vm.provision :puppet do |puppet|
   #   puppet.manifests_path = 'puppet/manifests'
   #   puppet.manifest_file = 'site.pp'
   #   puppet.module_path = 'puppet/modules'
   # end
 end

 # now provision Docker stuff
 config.vm.provision :docker
 config.vm.provision :docker_compose, yml: ["/vagrant/docker-compose.yml"], rebuild: true, project_name: "mysql", run: "always"


end

# node_config.vm.post_up_message = "System has provisioned successfully -- please validate the boxes ~cappetta"
