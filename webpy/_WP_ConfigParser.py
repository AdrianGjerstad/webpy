#!/usr/bin/env python3

########################################
# IMPORTS                              #
########################################

# A-Z STDLIB
import os
import string

# A-Z SOURCED
from _WP_Warnings import *

########################################
# FILE/DIRECTORY                       #
########################################

class file:
  def __init__(self, filepath):
    filepath = filepath.strip()
    if filepath == 'webpy://temp':
      self.path = ''
      self.temp_ = True
    else:
      if os.path.isfile(filepath):
        self.path = filepath
        self.temp_ = False
      else:
        self.path = 'webpy://notfound'
        self.temp_ = False

  def not_found(self):
    return self.path == 'webpy://notfound'

  def temp(self):
    return self.temp_

  def repr(self):
    return self.path

class directory:
  def __init__(self, filepath):
    filepath = filepath.strip()
    if filepath == 'webpy://temp':
      self.path = ''
      self.temp_ = True
    else:
      if os.path.isdir(filepath):
        self.path = filepath
        self.temp_ = False
      else:
        self.path = 'webpy://notfound'
        self.temp_ = False

  def not_found(self):
    return self.path == 'webpy://notfound'

  def temp(self):
    return self.temp_

  def repr(self):
    return self.path

########################################
# PARSE                                #
########################################

CONFIG_DEFAULTS = {
  'ipv4': '127.0.0.1',
  'port': 9009,
  'public': file('webpy://temp'),
  'shadow': file('webpy://temp'),
  'errorf': file('webpy://temp'),
  'index_gone': 'DIRLIST',
  'logsenabled': False,
  'logdir': directory('webpy://temp')
}

CONFIG_TYPES = {
  'ipv4': str,
  'port': int,
  'public': file,
  'shadow': file,
  'errorf': file,
  'index_gone': (str, file),
  'logsenabled': bool,
  'logdir': directory
}

def parse(filename):
  res = CONFIG_DEFAULTS.copy()
  with open(filename, 'r') as f:
    line = f.readline()
    ln = 1
    while line:
      line = line.split(';')

      for i in range(len(line)):
        line[i] = line[i].split('#')[0].strip()

      for r in line:
        if r == '': continue

        if len(r.split(':')) != 2:
          warn('Skipping line that does not have exactly one `:\'; line=%i' % (ln))
          continue

        rule_name = r.split(':')[0].rstrip()
        value_as_str = r.split(':')[1].lstrip()

        if len(rule_name) == 4:
          if rule_name[0] in string.ascii_lowercase:
            if rule_name[1] in string.digits and rule_name[2] in string.digits and rule_name[3] in string.digits:
              if res.get(rule_name, None) is None:
                res[rule_name] = [value_as_str]
              else: res[rule_name].append(value_as_str)
              continue

        type_ = CONFIG_TYPES.get(rule_name, None)
        if type_ == None:
          warn('Skipping line with unknown rule assignment; line=%i' % (ln))
          continue

        if isinstance(type_, tuple):
          for i in range(len(type_)):
            try:
              value = type_(value_as_str)
              break
            except:
              pass
        else:
          try:
            if type_ == list:
              value = value_as_str
            else: value = type_(value_as_str)
          except ValueError:
            if type_ == int:
              warn('Skipping line with innappropriate value type; line=%i' % (ln))

        if type_ == file or type_ == directory:
          if value.not_found():
            warn('File/directory not found; line=%i' % (ln))
        if type_ == list:
          if res[rule_name] == CONFIG_DEFAULTS[rule_name]:
            res[rule_name] = [value]
          else: res[rule_name].append(value)
        else:
          res[rule_name] = value

      line = f.readline()
      ln += 1

  return res
