from optparse import OptionParser
from random import random

opts,args = None,None
p_opts = None

def read_options():
	global opts,args
	
	p = OptionParser()
	p.add_option("-M","--model",metavar = "MODEL_PATH.py",
				action  = "store",
				dest    = "model_name",
				help    = "Model to be used for current experiment")
	
	p.add_option("-E","--extractor",metavar = "EXTRACTOR_PATH.py",
				action  = "store",
				dest    = "extractor_name",
				help    = "Extractor to be used for current experiment")
	
	p.add_option("-t","--test-file", metavar = "FILE",
				action  = "store",
				dest    = "test_file",
				help    = "file model will be evaluated on")
	p.add_option("-n","--name",metavar = "NAME",
				action  = "store",
				dest    = "experiment_name",
				help    = "Name given to experiment")
	p.add_option("-S","--pickled-extractor",metavar = "PICKLED_EXTRACTOR",
				action  = "store",
				dest    = "pickled_extractor",
				help    = "Pickled extractor to be used for current experiment\n\
							--extractor must be specified")

	p.add_option("-P","--pickled-model",metavar = "PICKLED_MODEL",
				action  = "store",
				dest    = "pickled_model",
				help    = "Pickled model to be used for current experiment\n\
							--model must be specified")
	p.add_option("-N","--window-size",metavar = "N",
				type    = "int",
				default = 1,
				action  = "store",
				dest    = "window_size",
				help    = "Window size to segment thread stream into")
	p.add_option("-B","--bandwidth",metavar = "BW",
				action  = "store",
				dest    = "bandwidth",type = "int",default = 1000,
				help    = "Bandwidth limit. Default is 1000")
	p.add_option("-v","--verbose",
				action  = "store_true",
				dest    = "verbose",
				help    = "print extra debug information")
	

	
	(opts,args) = p.parse_args()
	print opts,args
	if not opts.extractor_name:
		opts.extractor_name = opts.model_name
	
	if opts.experiment_name and opts.experiment_name.endswith('RANDOM'):
		opts.experiment_name = opts.experiment_name.replace(
										'RANDOM',
										str(random.randint(100,999)))
	return opts,args
import sys
def read_model_extractor_options(args,extractor=None,model=None):
	global p_opts
	p = OptionParser()
	try: extractor.opt_cfg(p)
	except: print "Extractor has no options"
	try: model.opt_cfg(p)
	except: print "Model has no options"

	p_opts,args = p.parse_args(args)
	print p_opts
	return args
	
if __name__=="__main__":
	read_options()


