REPORTS = None
SUBDIR = None
import sys,os
from datetime import datetime
def set_directory(directory):
	global SUBDIR
	SUBDIR = directory
	
def get_directory():
	global SUBDIR
	return SUBDIR
def reporting_init(options,directory):
	global SUBDIR,REPORTS
	REPORTS = directory
	SUBDIR = '%s/%s'%(directory,datetime.now().strftime('%Y%m%d%H%M') +\
								(' - %s'%options.experiment_name\
								 if options.experiment_name else ''))
	ensure_dir(SUBDIR)
	with open("%s/%s"%(SUBDIR,'command'),'w') as f:
		f.write(sys.executable)
		f.write(' ')
		f.write(sys.argv[0])
		for i in sys.argv[1:]:
			if i[0] == '-':
				f.write(' \\\n\t')
				f.write(i)
			else:
				f.write(' ')
				f.write('"%s"'%i)	
		f.write('\n')

def ensure_dir(f):
	if not os.path.exists('./%s'%f):
		os.makedirs(f)


def timestamp_log(*filenames):
	test = [open("%s/%s"%(SUBDIR,f),'w') for f in filenames]
	if len(test) == 1: return test[0]
	else: return test
	


def timestamp_model(*filenames):
	test = [open("%s/%s"%(SUBDIR,f),'wb') for f in filenames]
	if len(test) == 1: return test[0]
	else: return test
	
def write_value(key,value):
	with open("%s/%s"%(SUBDIR,key),'w') as f:f.write('%s\n'%value)
		
	
