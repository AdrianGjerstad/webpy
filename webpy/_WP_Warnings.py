#!/usr/bin/env python3

########################################
# IMPORTS                              #
########################################

# A-Z STDLIB
from datetime import datetime as dt
import sys

# A-Z SOURCED

########################################
# WARN                                 #
########################################

WARN_COLOR = True

def warn(*texts, sep=' ', end='\n', file=sys.stderr, flush=True, color=WARN_COLOR):
  if color:
    file.write('\033[1m\033[93m')
  file.write('[WARNING] [' + dt.now().strftime('%Y-%m-%dT%T.%fZ%z') + '] ' + sep.join(texts))
  if color:
    file.write('\033[0m')
  file.write(end)
  if flush:
    file.flush()

  return len(texts)

def error(*texts, sep=' ', end='\n', file=sys.stderr, flush=True, color=WARN_COLOR):
  if color:
    file.write('\033[1m\033[91m')
  file.write('[ERROR] [' + dt.now().strftime('%Y-%m-%dT%T.%fZ%z') + '] ' + sep.join(texts))
  if color:
    file.write('\033[0m')
  file.write(end)
  if flush:
    file.flush()

  return len(texts)
