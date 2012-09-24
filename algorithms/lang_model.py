
from utils.reader        import filter_tokenise
from sklearn.svm                     import SVR
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import SelectKBest,f_regression
import numpy as np
import itertools
epsilon = 0.1
count = 0
def memmapify(iterator,dtype,length):
	global count
	filename = "memmap%d.data"%count
	count += 1
	mm = None
	itemsize = np.dtype(dtype).itemsize
	vec_len = None
	for i,vec in enumerate(iterator):
		if mm == None:
			vec_len = len(vec)
			mm = np.memmap(
				filename,
				mode  = 'w+',
				shape = (vec_len,),
				dtype = dtype
			)
		else:
			mm = np.memmap(
					filename,
					offset = vec_len * i * itemsize,
					mode   = 'r+',
					shape  = (vec_len,),
					dtype  = dtype
			)
		mm[:] = vec[:]
	size = i+1
	return np.memmap(
			filename,
			mode = 'r',
			shape = (size,len(vec)),
			dtype = dtype
		)

class Extractor():

	def __init__(self):
		self.vectorizer = CountVectorizer(tokenizer=filter_tokenise)
		
	def opt_cfg(self,p):
		p.add_option("-K","--select-k-best",metavar = "DIM",
			dest    = "dimension", type = "int", default = 20,
			action  = "store",
			help    = "K best attributes")
	
	def train(self, records):
		self.DIM = DIM = 5
		self.feature_selector = SelectKBest(f_regression,k = DIM)
		count = sum(1 for _ in records.reset())
		print "Fitting vectorizer..."	
		self.vectorizer.fit(' '.join(window[2]) for window,_ in records.reset())
		y_vec = np.array([float(d_t) for _,d_t in records.reset()], dtype=np.float64)
		fs = self.feature_selector
		print "Fitting feature selector..."
		fs.fit(
			memmapify(
				(self.vectorizer.transform([' '.join(window[2])]).toarray()[0]
					for window,_ in records.reset()),
				dtype = np.float64,
				length = count
			),
			y_vec
		)
	def save(self):
		save_model('extractor',self)
	
	def finalise(self):
		DIM = self.DIM
		top_weights = list(np.argsort(self.feature_selector.scores_)[-DIM:])
		fn = self.vectorizer.get_feature_names()
		tokens  = [fn[i] for i in top_weights]
		tokens.reverse()
		self.vocab = tokens
	def extract(self,window):
		x = self.vectorizer.transform([' '.join(window[2])])
		x = x.toarray()
		l = np.sum(x)
		x = self.feature_selector.transform(x)
		#x = x.toarray()
		x = np.append(x,
				[
					l
				]
			)
		

		return x
		#if not self.done: self.corpus.append([' '.join(filter_tokenise(i)) for i in window[2]])

