#!/usr/bin/python

import os
import sys
import fnmatch

# check if the correct number of arguments is provided
if len(sys.argv) < 3 or len(sys.argv) < 3:
    print('Usage: script.py pattern path')
    exit(0)

walk_dir = sys.argv[2]
pattern = sys.argv[1]

for root, subdirs, files in os.walk(walk_dir):
    for filename in files:
        if fnmatch.fnmatch(filename, pattern):
            print(os.path.join(root, filename))
