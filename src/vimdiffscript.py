#!/usr/bin/python

""" This script is taken from stackoverflow with some updates."""

import os
import subprocess
import sys
import time


def vim_send(command, vim_server):
    subprocess.call(['vim',
                     '--servername',
                     vim_server,
                     '--remote-send',
                     command + '<Return>'
                     ])


vim_server = os.environ['VIM_SERVERNAME']
svn_orig_file = sys.argv[len(sys.argv) - 2]
modified_file = sys.argv[len(sys.argv) - 1]
vim_send(":tabnew", vim_server)
vim_send((":e " + modified_file), vim_server)
vim_send((":vertical diffsplit " + svn_orig_file), vim_server)

""" Waiting for 2 second is needed, as vim needs some time to load two files,
    but as soon as this scripts ends, svn deletes both files before vim could
    load it.
"""
time.sleep(2)
