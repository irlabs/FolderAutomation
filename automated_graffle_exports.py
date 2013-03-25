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

# This script goes through all the paths supplied in
# the settings file, resursively if needs be;
# Find all files of the type specified in the settings;
# Compares the modification date of the file to the
# modification date stored in the sqlite database;
# Filters only the new files or the modified once;
# And runs the supplied command with the file as argument.

# Watchdog detects file changes made with e.g. Textmate,
# but doesn't detect file changes from TextEdit and OmniGraffle.
# This is a major problem for this script, because it was primarily
# meant for .graffle files.
# The alternative strategy, which we're adopting is that of
# polling the modification times of the files we're interested in.

import sys, os, time, fnmatch
import file_watch_settings
import sqlite3 as lite
from subprocess import call

conn = None

def dbFilePath():
	"""
	Returns the file path of the sqlite database.
	"""
	return 'file_modifications.db'

def initDB():    
	"""
	Creates or just connects to the sqlite database
	"""
	global conn
	global c
	# Create the connection (and create the database if it wasn't here)
	conn = lite.connect(dbFilePath())
	c = conn.cursor()
	# Create the table structure
	c.execute("CREATE TABLE IF NOT EXISTS Files(Id INTEGER PRIMARY KEY, Path TEXT, Modified INTEGER);")
	conn.commit()

def hasBeenModified(filePath):
	"""
	Returns if the file has been modified since we've last looked.
	Also returns true if the file is new.
	"""
	modifiedTime = os.path.getmtime(filePath)
	c.execute("SELECT Id, Modified FROM Files WHERE Path=:Path;", {"Path": filePath})
	conn.commit()
	row = c.fetchone()
	# Check if this file is already in the database
	if (row):
		ID = row[0]
		modTime = row[1]
		if modifiedTime > modTime:
			c.execute("UPDATE Files SET Modified = ? WHERE Id = ?;", (modifiedTime, ID))
			conn.commit()
			return True
	else:
		# If the file is new, always return True
		c.execute("INSERT INTO Files(Path, Modified) VALUES (?, ?);", (filePath, modifiedTime))
		conn.commit()
		return True
	return False

def watchfolder(folderDict):
	"""
	Watches the folder for changes in specified files.
	"""
	# TODO: make this work with Omnigraffle folders as well
	path = os.path.expanduser(folderDict['path'])
	recursiveFlag = folderDict['recursive']
	processBundlesFlag = folderDict['processFileBundles']
	extension = "*.%s" % (folderDict['extension'])
	cmds = []
	cmds += folderDict['command'].split(' ')
	for root, dirnames, filenames in os.walk(path):
		if not recursiveFlag:
			if len(dirnames) > 0:
				dirnames.pop()
		for filename in fnmatch.filter(filenames, extension):
			filepath = os.path.join(root, filename)
			if hasBeenModified(filepath):
				cmds.append(filepath)
				call(cmds)

def main():
	initDB()
	# for folder in file_watch_settings.folders:
	# 	watchfolder(folder)
	try:
		while True:
			time.sleep(2)
			for folder in file_watch_settings.folders:
				watchfolder(folder)
	except KeyboardInterrupt:
		sys.exit()
	finally:
		print

if __name__ == '__main__':
	main()