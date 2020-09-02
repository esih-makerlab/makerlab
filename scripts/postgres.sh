#!/bin/bash

DKL_DIR=$(pwd)
WORK_DIR="$(cd "$(dirname "$0")" && pwd)"

source $WORK_DIR/_function.sh

################ ~ ENVIRONEMENT FILE
ENV_TEMPLATE=.env.template 

if [ ! -f .env ]; then
    echo ""
    print_info "- Creating environement file;"
    cp $ENV_TEMPLATE .env
fi

source .env

################ ~ SETTING UP POSTGRESQL 
sudo apt-get install postgresql postgresql-12-postgis-3 postgresql-contrib

function _psql {
    sudo -u postgres psql -c "$1"
}

# Grab database info from .env file
if [ -f .env ]; then
    source .env 
else
    print_error "!! Don't found environnement file: .env"
    exit 1;
fi

# Creating database if not already exists
# https://stackoverflow.com/questions/14549270/check-if-database-exists-in-postgresql-using-shell
if psql -lqt | cut -d \| -f 1 | grep -qw $DB_MK_NAME; then
    # database exists
    # $? is 0
    print_info "DELETING OLD $DB_MK_NAME DB"
    _psql "DROP DATABASE $DB_MK_NAME;"
fi

print_info "CREATING A NEW $DB_MK_NAME DB"

_psql "CREATE DATABASE $DB_MK_NAME;"

# https://stackoverflow.com/questions/8546759/how-to-check-if-a-postgres-user-exists
if psql -t -c '\du' | cut -d \| -f 1 | grep -qw $DB_MK_USER; then
    # user exists
    # $? is 0
    _psql "DROP USER $DB_MK_USER;"
fi

_psql "CREATE USER $DB_MK_USER WITH ENCRYPTED PASSWORD '$DB_MK_PASSWORD';"
_psql "GRANT ALL PRIVILEGES ON DATABASE $DB_MK_NAME TO $DB_MK_USER;"
_psql "\connect $DB_MK_NAME;"
_psql "ALTER USER $DB_MK_USER WITH SUPERUSER;"

################ ~ MIGRATE DATABASE
print_info "- Migrate database"
venv/bin/python manage.py migrate

print_info "INSTALLATION RÉUSSIE"