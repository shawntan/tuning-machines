'''
Created on Jul 19, 2012

@author: shawn
'''
from lib.io.reporting	import get_directory
from lib.options		import read_options
from lib.io.reader		import windowed
from lib.io.util		import load_from_file

import pickle
def save_model(filename,model):
	f = open("%s/%s"%(get_directory(),filename),'wb')
	pickle.dump(model,f)
	f.close()

def unpickle_model(filepath):
	return pickle.load(filepath)

if __name__ == '__main__':
	o,args = read_options()
	extractor   = load_from_file(o['extractor_name'], "Extractor")
	for window,d_t in windowed([o['test_file']],o['window_size']):
		print  extractor.extract(window),d_t
	extractor.save()