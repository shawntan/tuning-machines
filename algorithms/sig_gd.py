import numpy as np
import math
class GradientDescent():
	function = lambda self,z: 1/(1 + math.exp(-z))
	gradient = lambda self,z: self.function(z)*(1 - self.function(z))
	def __init__(self,dim,alpha,epsilon,max_time,verbose = False):
		self.dim = dim = dim + 1
		self.weights = np.zeros(dim)#np.random.uniform(0,1,dim)
		self.weights[-1] = 1
		self.alpha = alpha
		self.epsilon = epsilon
		self.verbose = verbose
		self.max_time = max_time
	def preproc_vec(self,vec):
		if vec.shape[0] == self.dim: return vec
		else: return np.append(vec,[1])
	def update(self,vec,y):
		vec = self.preproc_vec(vec)
		#print "\t",vec,y
		error = self.func(vec) - y
		#if abs(error) < self.epsilon: return
		if self.verbose:
			print "%s o\n%s\n = %0.20f,\terror=%s"%(
					self.weights,
					vec,
					self.func(vec),
					error
				)
		weights = np.zeros(self.dim,dtype=np.float64)
		for i,w in enumerate(self.weights):
			delta = self.alpha *\
					error *\
					self.gradient(np.dot(self.weights,vec)) *\
					vec[i]
			weights[i] = self.weights[i] - delta
		self.weights = weights
	def func(self,vec):
		return self.max_time * self.function(np.dot(self.weights,vec))
	def predict(self,vec, y = None):
		vec = self.preproc_vec(vec)
		pred = self.func(vec)
		return pred

from itertools import permutations
if __name__ == '__main__':
	gd = GradientDescent(
			2,0.2,0.000001,300,
			verbose = True)
	fun = lambda vec: 300 if (vec[0] or vec[1]) else 0
	for _ in range(10000):
		for i in [(0,0),(0,1),(1,0),(1,1)]:
			val = np.array(i) 
			gd.update(val,fun(val))

	print gd.predict(np.array([1,0]))
	print gd.predict(np.array([1,1]))
	print gd.predict(np.array([0,1]))
	print gd.predict(np.array([0,0]))
