#!/usr/bin/env python

# Add project path to system's python path,
# so we can find and import the pymocap package
import os, sys

thisdir = os.path.dirname(__file__)
projectdir = os.path.abspath(os.path.join(thisdir, '..'))

if projectdir not in sys.path:
  sys.path.insert(0, projectdir)

if __name__ == '__main__':
    import subprocess
    os.chdir(thisdir)
    subprocess.call(['python', '-m', 'unittest', 'discover'])