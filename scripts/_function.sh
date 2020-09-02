#!/bin/bash
function print_info {
    if [[ "$2" == "--bold" ]]; then
        echo -en "\033[36;1m"
    else
        echo -en "\033[0;36m"
    fi
    echo "$1"
    echo -en "\033[00m"
}


function print_error {
    echo -en "\033[31;1m"
    echo "$1"
    echo -en "\033[00m"
}


function _in {
  # credits: https://stackoverflow.com/a/8574392
  local e match="$1"
  shift
  for e; do [[ "$e" == "$match" ]] && return 0; done
  return 1
}

# load nvm
function load_nvm {
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
}