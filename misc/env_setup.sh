#!/usr/bin/env bash
#setup the virtualenv

#pip install flask
#pip install sqlalchemy
#pip install requests

#if not installed
# sudo apt-get install python3-dev
# sudo apt-get install libmysqlclient-dev
# sudo apt-get install zlib1g-dev
#
#pip3 install mysqlclient

export CARIBA_MYSQL_USER="cariba_dev"
export CARIBA_MYSQL_PWD="cariba_dev_pwd"
export CARIBA_MYSQL_HOST="localhost"
#this is for the testing db
export CARIBA_MYSQL_DB="cariba_dev_db"
