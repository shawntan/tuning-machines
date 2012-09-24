import numpy as np
from sklearn import linear_model
from itertools import permutations
from lang_model import Extractor
from utils.reader import *
import csv,sys

count = 0

clf = linear_model.LinearRegression()
filenames = [sys.argv[1]]
filename_x = "X"
filename_y = "Y"
window_size = 15

e = Extractor()
count = sum(1 for _ in windowed(filenames,window_size))

class RewinderWindow():
	def __init__(self,filenames,window_size):
		self.filenames = filenames
		self.window_size = window_size
	def reset(self):
		return windowed(self.filenames,self.window_size)
e.train(RewinderWindow(filenames,window_size))
e.finalise()


def first(vec_size,vec_count):
	X = np.memmap(
			filename_x,
			mode = 'w+',
			shape = (vec_count,vec_size),
			dtype="float64"
		)
	Y = np.memmap(
			filename_y,
			mode  = "w+",
			shape = (vec_count,),
			dtype = "float64"
		)
	return X,Y
X,Y = None,None
for i,instance in enumerate(windowed(filenames,window_size)):
	window, d_t = instance
	x_vec = e.extract(window)
	if i == 0:  X,Y = first(len(x_vec),count)
	X[i][:] = x_vec[:]
	Y[i] = d_t

print X, X.shape
print Y, Y.shape



