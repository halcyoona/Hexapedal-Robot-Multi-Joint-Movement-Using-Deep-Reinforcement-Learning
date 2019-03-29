# Modified version of https://rosettacode.org/wiki/Keyboard_input/Keypress_check#Python
# Just call getch() in a given loop

from __future__ import absolute_import, division, unicode_literals, print_function

import sys
if sys.version_info.major < 3:
	import thread as _thread
else:
	import _thread
import time
 
 
try:
	from msvcrt import getch  # try to import Windows version
except ImportError:
	import tty, termios
	
	def getch():   # define non-Windows version
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch