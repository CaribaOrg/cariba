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
export CARIBA_MYSQL_DB="cariba_dev_db"

export MAIL_SERVER="mail.fuzzfoo.tech"
export MAIL_PORT=465
export MAIL_USE_SSL="False"
export MAIL_USE_TLS="True"
export MAIL_USERNAME="noreply@fuzzfoo.tech"
export MAIL_PASSWORD="gPXyczHNmbe3"
export MAIL_DEFAULT_SENDER="noreply@fuzzfoo.tech"