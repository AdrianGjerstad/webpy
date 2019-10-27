#!/usr/bin/env python3

########################################
# IMPORTS                              #
########################################

# A-Z STDLIB
from http.server import BaseHTTPRequestHandler, HTTPServer
import multiprocessing
import os
import sys

# A-Z SOURCED
from _WP_Warnings import *

########################################
# GLOBALS                              #
########################################

global httpd
httpd = None

########################################
# REQUEST HANDLER                      #
########################################

class _WP_RequestHandler(BaseHTTPRequestHandler):
  pass

########################################
# SERVER                               #
########################################

class _WP_Server(HTTPServer):
  pass

########################################
# SERVER SPAWNER                       #
########################################

def _WP_ServerSpawner():
  global httpd
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    httpd.shutdown()

########################################
# MAIN                                 #
########################################

def main(conf):
  global httpd
  httpd = _WP_Server(('127.0.0.1', 9009), _WP_RequestHandler)

  server_proc = multiprocessing.Process(target=_WP_ServerSpawner)
  server_proc.start()

  try:
    server_proc.join()
  except KeyboardInterrupt:
    server_proc.terminate()
    server_proc.join()

  return 0

########################################
# __NAME__ GUARD                       #
########################################

if __name__ == '__main__':
  conf = None
  if len(sys.argv) == 1:
    warn('No config file specified. Using default config file.')
    conf = os.environ['WEBPY_PATH'] + '/default.conf'
  elif len(sys.argv) > 2:
    warn('WebPy only accepts one argument.')

  if conf is None:
    if os.path.isfile(sys.argv[1]) and sys.argv[1].startswith('/'):
      conf = sys.argv[1]
    else:
      error('[Errno 100] No file exists at ' + sys.argv[1] + '. Is there no leading slash?')
      sys.exit(100)

  exit_code = main(conf)
  if exit_code is None: exit_code = 255

  sys.exit(exit_code)
else:
  error('[Errno 200] Cannot run WebPy through imports.')
  sys.exit(200)
