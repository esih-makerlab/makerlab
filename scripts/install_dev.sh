#!/bin/bash

DKL_DIR=$(pwd)
WORK_DIR="$(cd "$(dirname "$0")" && pwd)"
DISTRO_NAME=$(lsb_release -sc)
OS_REQUIREMENTS_FILENAME="requirements-$DISTRO_NAME.apt"

source $WORK_DIR/_function.sh

function activate_venv {
    . venv/bin/activate
}

########################### ~ INSTALL OS DEPENDENCIES
print_info "Installig os dependencies" "--bold"


# Check if a requirements file exist for the current distribution.
if [ ! -r "$WORK_DIR/$OS_REQUIREMENTS_FILENAME" ]; then
    cat <<-EOF >&2
		There is no requirements file for your distribution.
		You can see one of the files listed below to help search the equivalent package in your system:
		$(find ./ -name "requirements-*.apt" -printf "  - %f\n")
	EOF
    exit 1;
fi

LIST_PKG=$(grep -v "#" "$WORK_DIR/$OS_REQUIREMENTS_FILENAME" | grep -v "^$")

print_info "Updating package installed"
sudo apt-get update

# installing pkg
for PKG in $LIST_PKG
    do 
        print_info "Installing $PKG"
        sudo apt-get install $PKG
done


print_info "Cleaning package installed"
sudo apt-get clean

#################### ~  PYTHON DEPENDENCIES
print_info "Install python dependencies" "--bold" 
DKL_VENV="venv"

if [ ! -f $DKL_VENV/bin/activate ]; then
    if [ -d $DKL_VENV ]; then
        print_info "!! Find corrupted virtualenv folder without bin/activate"

    print_info "remove $(realpath $DKL_VENV)"
    rm -r $DKL_VENV
    else
        print_error "We recommend to delete this folder, press \`y\` to delete this folder"
        echo -n "Choice : "
        read -n 1
        echo ""
        if [[ $REPLY == "y" ]]; then
            print_info "remove $(realpath $DKL_VENV)"
            rm -r $DKL_VENV
        else
            print_error "!! Cannot continue. Move, rename or delete this folder before retry"
            exit 1
        fi
    fi


    print_info "* [+virtualenv] installing \`virtualenv 16.2.0\` with pip"
    pip3 install --user virtualenv==16.2.0

    print_info "* [+virtualenv] creating virtualenv"
    err=$(python3 -m venv $DKL_VENV )
    if [[ $err != "" ]]; then
        exVal=1
        if [[ $err == *"ensurepip"* ]]; then # possible issue on python 3.6
            print_info "!! Trying to create the virtualenv without pip"
            python3 -m venv $DKL_VENV --without-pip; exVal=$?
        fi

        if [[ $exVal != 0 ]]; then
            print_error "!! Cannot create (use \`-virtualenv\` to skip)"
            print_info "You can try to change the path of venv folder before retrying this command with \`export DKL_VENV=../venv\`"
            exit 1
        fi
    fi
fi

if [ ! -f $DKL_VENV/bin/activate ]; then
    echo ""
    print_error "!! No virtualenv, cannot continue"
    print_info "- Install virtualenv with \`+virtualenv\` (recommanded) ;"
    exit 1
fi

source $DKL_VENV/bin/activate; exVal=$?

if [[ $exVal != 0 ]]; then
    echo ""
    print_error "!! Cannot load virtualenv"
    print_info "- Reinstall virtualenv with \`+virtualenv\` (recommanded) ;"
    exit 1
fi 

pip3 install -r requirements.txt


source $WORK_DIR/_function.sh

print_info "Installing dev envirronement..." "--bold"


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
if psql -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    # database exists
    # $? is 0
    print_info "DELETING OLD $DB_NAME DB"
    _psql "DROP DATABASE $DB_NAME;"
fi

print_info "CREATING A NEW $DB_NAME DB"

_psql "CREATE DATABASE $DB_NAME;"

# https://stackoverflow.com/questions/8546759/how-to-check-if-a-postgres-user-exists
if psql -t -c '\du' | cut -d \| -f 1 | grep -qw $DB_USER; then
    # user exists
    # $? is 0
    _psql "DROP USER $DB_USER;"
fi

_psql "CREATE USER $DB_USER WITH ENCRYPTED PASSWORD '$DB_PASSWORD';"
_psql "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
_psql "\connect $DB_NAME;"
_psql "ALTER USER $DB_USER WITH SUPERUSER;"

################ ~ MIGRATE DATABASE
print_info "- Migrate database"
venv/bin/python manage.py migrate

print_info "INSTALLATION RÉUSSIE"