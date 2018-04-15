#!/usr/bin/env bash

# Main packages
sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get install git
sudo apt-get install mysql-client
sudo apt-get install nginx
sudo apt-get install supervisor
sudo apt-get install python-pip python3-pip
#sudo apt-get install redis-server
#sudo apt-get install rabbitmq-server

# Typical problems
sudo apt-get install libmysqlclient-dev
sudo apt-get install python3-dev

# Remove previous repositiory and download a new one
sudo rm -r ~/Coconut/mycoconut
git clone https://github.com/salvacarrion/mycoconut.git

# Virtual environment
#export LC_ALL=C  # Typical problem
sudo pip install virtualenv
cd ~/Coconut/
virtualenv --python=python3 venv-coconut
source venv-coconut/bin/activate

# Install the minimum required dependencies first
cd mycoconut
pip install -r requirements.txt