'''
Created on Sep 24, 2012

@author: shawn
'''
from lib.options.config import configuration as config
import __builtin__

def marked_open(*params):
	global _open
	print "Opening file with marked_open", params[1]
	print config.filename_formats.date
	return _open(*params)

_open = __builtin__.open
__builtin__.open = marked_open

