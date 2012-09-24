from utils.reader    import windowed
from utils.reporting import *
from utils.util      import *
import pickle,math,getopt
from evaluate_window import evaluate as evaluate_window
from utils.options import read_options, read_model_extractor_options
def train(model,extractor,iterator,window_size,iterations = 1):
	for _ in range(iterations):
		model.train(iterator)
	model.finalise()
	return model.save()
	"""
	f = timestamp_model('model')
	pickle.dump(model,f)
	f.close()
	"""


def performance(model,extractor,rest_instances,window_size,verbose,model_file):
	print "Calculating MAPE"
	print "====================="
	total_percent_error = 0
	count = 0
	for fv,d_t in rest_instances:
		p = model.predict(fv)
		if d_t > 0:
			percent_error = math.fabs(float(p - d_t)/d_t)
			if verbose: print "delta_t: %d\tpredicted: %d\tAPE: %0.2f"%(
					d_t,
					p,
					percent_error
				)
			total_percent_error += percent_error
			count += 1

	ave_percentage_error = total_percent_error/count
	
	return ave_percentage_error



def train_extractor(extractor,filenames,window_size):
	extractor.train(windowed(filenames,window_size))
	extractor.finalise()
	return extractor.save()

def file_len(fname):
	with open(fname) as f:
		for i, l in enumerate(f):
			pass
	return i + 1

from evaluate import evaluate
if __name__ == "__main__"
'Visit/Post':
	o,args = read_options()
	reporting_init(o,"pickled_models")
	extractor   = load_from_file(o.extractor_name, "Extractor")
	model       = load_from_file(o.model_name,"Model",o)
	args = read_model_extractor_options(args,extractor,model)

	
	print "Training extractor..."
	if hasattr(extractor,'train'):
		train_extractor(   extractor,args,o.window_size)

	instances = [i for i in extracted_vecs(extractor,args[0],o.window_size)]
	instance_count = len(instances)
	if instance_count < 2:
		print "Insufficient instances"
		sys.exit()
	reporting_init(o,"pickled_models")
	train_count = int(instance_count*0.75)
	trainset,testset = instances[:train_count],instances[train_count:]
	#trainset,testset = instances,instances
	#print trainset
	print "Instance split:",len(trainset),len(testset)
	
	print "Training model..."
	filename = train(
				model,
				extractor,
				trainset,
				o.window_size)
	
	print "Evaluating..."
	ave_percentage_error = performance(model,extractor,testset,o.window_size,o.verbose,filename)
	print ave_percentage_error
	model.add_experiment('regression_test(partial thread)',filename,ave_percentage_error)
	result =  evaluate(args[0], model, extractor, o.window_size, o.bandwidth,
					offset = train_count,
					sliding_window_size=sum(i for _,i in trainset)/len(trainset),
					verbose = o.verbose)
	result['filename'] = args[0]
	result['offset'] = train_count
	print model.experiments
	model.add_experiment('visit_evaluation',filename,result)
	model.save()
