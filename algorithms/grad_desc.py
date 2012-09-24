import numpy as np

class GradientDescent():
	def __init__(self,dim,alpha,epsilon,verbose = False):
		self.dim = dim = dim + 1
		self.weights = np.zeros(dim)
		self.weights[-1] = 1
		self.alpha = alpha
		self.epsilon = epsilon
		self.verbose = verbose
	def preproc_vec(self,vec):
		if vec.shape[0] == self.dim: return vec
		else: return np.append(vec,[1])
	def update(self,vec,y):
		vec = self.preproc_vec(vec)
		#print "\t",vec,y
		error = self.predict(vec) - y
		#if abs(error) < self.epsilon: return
		if self.verbose:
			print "%s.%s=%0.2f,\terror=%s"%(self.weights,vec,self.func(vec),error)
		weights = np.zeros(self.dim)
		for i,w in enumerate(self.weights):
			delta = self.alpha * vec[i] * error
			weights[i] = self.weights[i] - delta
		self.weights = weights
	def func(self,vec):
		return np.dot(self.weights,vec)
	def predict(self,vec, y = None):
		vec = self.preproc_vec(vec)
		pred = self.func(vec)
		return pred
	

from itertools import permutations
if __name__ == '__main__':
	gd = GradientDescent(2,0.0001,0.000001)
	fun = lambda vec: 2*vec[0] + 3*vec[1]
	for i in permutations(range(100),2):
		val = np.array(i) 
		gd.update(val,fun(val))
