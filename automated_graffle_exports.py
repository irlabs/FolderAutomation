#!/usr/bin/env python
# encoding: utf-8
"""
automated_graffle_exports.py

Created by Dirk van Oosterbosch on 2013-02-16.
Copyright (c) 2013 IR Labs, Amsterdam. All rights reserved.
"""

# Use settings file:
#	path
#	recursive
#	extension
#	command

# Run this script as a daemon (with launchd)
# Find all files of type '.graffle'
# Define default export file
# Filter only files of which the modified date is later than default export file
# Run the file through applescript

# Watchdog detects file changes made with e.g. Textmate,
# but doesn't detect file changes from TextEdit and OmniGraffle.
# This is a major problem for this script, because it was primarily
# meant for .graffle files.
# We need to adopt a new strategy of polling the modification times of
# the files we're interested in, and comparing them with ... with what?
# With the modification times of the files stored in a sqlite db?

import sys, os, time, fnmatch
import file_watch_settings
import sqlite3 as lite

def main():
	observerList = []
	for folder in file_watch_settings.folders:
		path = os.path.expanduser(folder['path'])
		recursiveFlag = folder['recursive']
		for root, dirnames, filenames in os.walk(path):
			if not recursiveFlag:
				if len(dirnames) > 0:
					dirnames.pop()
			print root, dirnames, filenames
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		sys.exit()
	print

if __name__ == '__main__':
	main()