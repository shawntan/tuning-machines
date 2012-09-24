'''
Created on Jul 19, 2012

@author: shawn
'''
from lib.io.reporting import get_directory

import pickle
def save_model(filename,model):
	fullpath = "%s/%s"%(get_directory(),filename)
	f = open(fullpath,'wb')
	pickle.dump(model,f)
	f.close()
	return fullpath

def unpickle_model(filepath):
	return pickle.load(filepath)

