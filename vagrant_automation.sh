#!/bin/bash
echo Launching the Box without provisioning
vagrant up --no-provision
echo Starting Shell Provisioning
vagrant provision --provision-with shell
echo Starting Puppet Provisioning
vagrant provision --provision-with puppet
echo Starting Docker Provisioning
vagrant provision --provision-with docker
echo Starting Docker-Compose Provisioning
vagrant provision --provision-with docker_compose
echo Reloading Vagrant
vagrant reload
