from utils.reader    import windowed
from utils.reporting import *
from utils.util      import *
from regression_performance import performance
import pickle,math,getopt

def train(model,extractor,filenames,window_size,iterations = 1):
	for _ in range(iterations):
		for f in filenames:
			try:
				model.train(extracted_vecs(extractor,f,window_size))
			except ValueError as e:
				raise e
				
	model.finalise()
	return model.save()
	"""
	f = timestamp_model('model')
	pickle.dump(model,f)
	f.close()
	"""

def train_extractor(extractor,filenames,window_size):
	extractor.train(windowed(filenames,window_size))
	extractor.finalise()
	return extractor.save()

if __name__ == "__main__":
	o,args = read_options()
	reporting_init(o,"pickled_models")
	extractor   = load_from_file(o.extractor_name, "Extractor")
	model       = load_from_file(o.model_name,"Model",o)
	
	if hasattr(extractor,'train'):
		train_extractor(   extractor,args,o.window_size)
	filename = train(model,extractor,args,o.window_size)
	print performance(model,extractor,[o.test_file],o.window_size,o.verbose,filename)
