#!/usr/bin/env python
# encoding: utf-8
"""
file_watch_settings.py

Created by Dirk van Oosterbosch on 2013-02-16.
Copyright (c) 2013 IR Labs, Amsterdam. All rights reserved.
"""

# Folders to watch
folders = [
	{ 	'path':				'~/Desktop/TestFolder',
		'recursive':		True,
		'extension':		'txt',
		'command':			'echo' },
	{ 	'path':				'~/Desktop/TestFolder',
		'recursive':		True,
		'extension':		'graffle',
		'command':			'osascript /Users/dirk/Developer/Python/FolderAutomation/omnigraffle_export.scpt' },
]