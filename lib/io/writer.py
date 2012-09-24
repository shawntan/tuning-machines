'''
Created on Sep 24, 2012

@author: shawn
'''
import __builtin__
_open = __builtin__.open
def marked_open(*params):
	global _open
	print "Opening file with marked_open", params[1]
	return _open(*params)
__builtin__.open = marked_open

