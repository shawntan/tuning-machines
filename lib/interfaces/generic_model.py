'''
Created on Jul 17, 2012

@author: shawn
'''

import md5
from model_utils import save_model
from collections import defaultdict

class GenericModel(object):
	epsilon = 0.1
	def __init__(self,o):
		self.options = o
		self.experiments = defaultdict(list)

	def predict(self,feature_vec = None, d_t = None, current_d_t = None):
		pred = self.avg
		if current_d_t:
			k = 0
			while k*self.avg + pred <= current_d_t + self.epsilon: k += 1
			return k*self.avg + pred
		else:
			return pred
	
	def ensure_prediction_conditions(self,pred,feature_vec,d_t,current_d_t):
		if current_d_t:
			if pred > current_d_t + self.epsilon:
				return pred
			else:
				return GenericModel.predict(self,feature_vec,d_t,current_d_t)
		else:
			return pred

	def add_experiment(self,test_type,test_files,result):
		if hasattr(test_files,'sort'):
			test_files.sort()
			names = '\n'.join(test_files)
		else:
			names = test_files
			key = md5.new(names).hexdigest()
			self.experiments[key].append((test_type,test_files,result))
	
	def save(self):
		return save_model('model', self)
