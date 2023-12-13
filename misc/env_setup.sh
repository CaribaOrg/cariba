#!/usr/bin/env bash
#setup the enviroenement variables

#database
export CARIBA_MYSQL_USER="root"
export CARIBA_MYSQL_PWD="root"
export CARIBA_MYSQL_HOST="localhost"
export CARIBA_MYSQL_DB="cariba_test_db" #db name

#mail
export MAIL_SERVER="your_mail_server"
export MAIL_PORT=465
export MAIL_USE_SSL="False"
export MAIL_USE_TLS="True"
export MAIL_USERNAME="your_mail_username"
export MAIL_PASSWORD="your_mail_password"
export MAIL_DEFAULT_SENDER="your_default_mail_sender"

#paypal
export PAYPAL_SANDBOX_BUSINESS_SECRET="your_paypal_sandbox_business_secret"
export PAYPAL_SANDBOX_BUSINESS_CLIENT_ID="your_paypal_sandbox_business_client_id"

#security
export SECURITY_PASSWORD_SALT="your_security_password_salt"
export DEBUG="False"
export SECRET_KEY="your_secret_key"