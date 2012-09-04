import numpy as np
from sklearn import linear_model
from itertools import permutations
clf = linear_model.LinearRegression()
filename = "raibbish"
fp = np.memmap(
		filename,
		mode = 'w+',
		shape = (999000,2),
		dtype="float64"
	)
fp[:] = [(i,j) for i,j in permutations(range(0,1000),2)][:]
w     = np.array([3,4])
res   = np.array([np.dot(w,v) for v in fp])
print fp 
del fp

fp = np.memmap(filename, shape = (999000,2), mode='r', dtype="float64")
print fp

clf.fit(fp,res)
print clf.predict([1,0])
print clf.predict([0,1])
print clf.predict([1,1])
print clf.predict([0,0])
