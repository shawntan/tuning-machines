import cPickle as pickle
class pickled_globals(object):
	def __init__(self,pg_dir):
		self.pg_dir = pg_dir 
	def __getattr__(self, attr_name):
		"""
		Loads the file from pg_dir into an object,
		then caches the object in memory.
		"""
		obj = pickle.load(open('%s/%s'%(self.pg_dir,attr_name),'rb'))
		self.__setattr__(attr_name,obj)
		return obj

pg = pickled_globals('working')
