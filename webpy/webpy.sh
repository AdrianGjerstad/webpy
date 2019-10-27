#!/usr/bin/env bash

function webpy() {
  command python3 > /dev/null 2>&1

  if [[ $? -eq 127 ]]; then
    echo 'Python3 is required to run WebPy. Please download Python3. Aborting...'
    return 150
  fi

  if [[ $WEBPY_PATH == '' ]]; then
    echo 'Where is your WebPy program installed?'
    read WEBPY_PATH

    if [[ $WEBPY_PATH != '/'* ]]; then
      WEBPY_PATH='${PWD}/${WEBPY_PATH}'
    fi

    if [[ ! -d $WEBPY_PATH ]]; then
      echo 'That is not a path that exists.'
      return 152
    fi

    export WEBPY_PATH
  fi

  if [[ $WEBPY_PATH == *'/' ]]; then
    lengthm1=${${#WEBPY_PATH}-1}
    echo $WEBPY_PATH | cut -c-$lengthm1
  fi
}
