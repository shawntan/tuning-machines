'''
Created on Sep 24, 2012

@author: shawn
'''
from lib.options.config import configuration as config
import __builtin__

class FileWrapper(object):
	def __init__(self,obj):
		self.obj = obj
	
	def close(self,*args,**kwargs):
		print "Closing file..."
		self.obj.close(*args,**kwargs)

	def __defattr__(self,attr):
		if hasattr(self.obj, attr):
			attr_value = getattr(self.obj,attr)
			if isinstance(attr_value,types.MethodType):
				def callable(*args, **kwargs):
					return attr_value(*args, **kwargs)
				return callable
			else:
				return attr_value
		else:
			raise AttributeError


def marked_open(*params):
	global _open
	print "Opening file..."
	print config.filename_formats.date
	return _open(*params)

_open = __builtin__.open
__builtin__.open = marked_open

