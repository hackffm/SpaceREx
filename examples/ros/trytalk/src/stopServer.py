#!/usr/bin/env python
import psutil
from subprocess import Popen

for process in psutil.process_iter():
	if process.cmdline == ['python', 'server.py']:
		print('server.py found.Terminating it.')
		process.terminate()
		break
	else:
		print(process.cmdline)

print('done')
