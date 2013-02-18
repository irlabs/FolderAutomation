import os, sys
import time

for root, dirnames, filenames in os.walk('/Users/dirk/Desktop/TestFolder'):
	print root, dirnames, filenames
print "--------"
for a in next(os.walk('/Users/dirk/Desktop/TestFolder')):
	print a
print "--------"
for root, dirnames, filenames in os.walk('/Users/dirk/Desktop/TestFolder'):
	if len(dirnames) > 0:
		dirnames.pop()
	print root, dirnames, filenames
try:
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	sys.exit()
