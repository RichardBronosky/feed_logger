#!/usr/bin/env python

import json
import os
import re
import shutil
import subprocess
import urllib2
from functools import partial
from multiprocessing.dummy import Pool as ThreadPool

# preliminary work for configurable* storage paths
# * this script has only been used to store and commit feeds to the current directory and git instance
PID_DIR = os.path.realpath('pids')
PID_FILE_FORMAT = os.path.join(PID_DIR, '{name}')
OUTPUT_DIR_FORMAT = os.path.realpath('feeds')
OUTPUT_FILE_FORMAT = os.path.join(OUTPUT_DIR_FORMAT, '{name}.json')

feeds = json.load(open('feeds.json'))


# the last worker commits the changes
def commit():
    subprocess.Popen(['git', 'add', OUTPUT_DIR_FORMAT], stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()
    out = subprocess.Popen(['git', 'status', '--porcelain', '-z'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    # grep the porcelain output for staged modifications and commit if any are found
    if len(re.findall('(^|\x00)[AM]', out[0])) > 0:
        subprocess.Popen(['git', 'commit', '--allow-empty-message', '--message', ''], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# this is the job all workers do
def collect(name, url):
    # get the feed and write it (currently very json specific)
    json.dump(json.load(urllib2.urlopen(url)), open(OUTPUT_FILE_FORMAT.format(name=name), 'w'), indent=4)
    # touch a file to indicate that the work it complete
    open(PID_FILE_FORMAT.format(name=name), 'a').close()
    # each worker checks to see if it is the last and cleans up after itself if so
    if len([name for name in os.listdir(PID_DIR) if os.path.isfile(os.path.join(PID_DIR, name))]) == len(feeds):
        commit()
        shutil.rmtree(PID_DIR)

# prevent concurrent processes
if os.path.exists(PID_DIR):
    raise OSError(1, 'Refusing to continue because it appears another process is currently running or has left its working directory in place', PID_DIR)
else:
    os.makedirs(PID_DIR)

# Make dirs if they don't exist
map(lambda directory: os.makedirs(OUTPUT_DIR_FORMAT.format(name=directory)) if not os.path.exists(OUTPUT_DIR_FORMAT.format(name=directory)) else None, feeds.keys())

# distribute work over threads
pool = ThreadPool(4)
pool.map(partial(apply, collect), feeds.iteritems())
