Folder Automation
=================

A simple python tool to watch folders for specific files and perform a command if files are created or modified. **This tool is specifically targeted on OS X**.

This tool uses polling and not the [watchdog](https://github.com/gorakhargosh/watchdog) module. Although watchdog is a great module to write such an automation tool, file changes made by certain applications on OS X (e.g. *TextEdit* or *OmniGraffle*) are not detected by FSEvents (File System Events), the OS X system framework which is used by watchdog. On save, these applications write the changes to a temporary file, and then on success rename this temporary file onto the old file, thereby bypassing fsevent.

Install as Daemon
-----------------

