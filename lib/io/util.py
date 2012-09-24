from reader import windowed
import sys, imp, traceback, md5, pickle

def load_from_file(filepath,class_name,*params):
	class_inst = None

	"""
	mod_name,file_ext = os.path.splitext(os.path.split(filepath)[-1])
	if file_ext.lower() == '.py':
		py_mod = imp.load_source(mod_name, filepath)
	elif file_ext.lower() == '.pyc':
		py_mod = imp.load_compiled(mod_name, filepath)
	"""

	try:
		try:
			#code_dir  = os.path.dirname(filepath)
			#code_file = os.path.basename(filepath)
			fin = open(filepath, 'rb')
			module_name = md5.new(filepath).hexdigest()
			py_mod = imp.load_source(module_name, filepath, fin)
			print "%s loaded as %s"%(filepath,module_name)
		finally:
			try: fin.close()
			except: pass
	except ImportError:
		traceback.print_exc(file = sys.stderr)
		raise
	except:
		traceback.print_exc(file = sys.stderr)
		raise

	if hasattr(py_mod, class_name):
		class_ = getattr(py_mod,class_name)
		class_inst = class_(*params)
	
	return class_inst


def extracted_vecs(extractor, filename, window_size, first = None):
	for window,d_t in windowed([filename],window_size):
		feature_vec = extractor.extract(window)
		yield feature_vec,d_t





