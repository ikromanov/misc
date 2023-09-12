  #!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import subprocess

"""Copy Special exercise
"""

# +++your code here+++
# Write functions and modify main() to call them
def get_special_paths(dirname):
  result = []
  paths = os.listdir(dirname)
  for file in paths:
    match = re.search(r'__(\w+)__',file)
    if match:
      result.append(os.path.abspath(os.path.join(dirname, file)))
  return result

def copy_to(paths, to_dir):
  if not os.path.exists(to_dir):
    os.mkdir(to_dir)
  for path in paths:
    fname = os.path.basename(path)
    shutil.copy(path, os.path.join(to_dir, fname))

#def zip_to(paths, to_dir):


def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print("usage: [--todir dir][--tozip zipfile] dir [dir ...]")
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  source_dir = args[0]

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    source_dir = args[2]
    del args[0:2]

  tozip = ''
  if args[0] == '--tozip':
    tozip = args[1]
    source_dir = args[2]
    del args[0:2]

  if len(args) == 0:
    print("error: must specify one or more dirs")
    sys.exit(1)

  # +++your code here+++
  # Call your functions
  paths = get_special_paths(source_dir)
  if todir:
    copy_to(paths,todir)

if __name__ == "__main__":
  main()
