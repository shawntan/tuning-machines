	#!/usr/bin/python2
from lib.io.reader				import windowed
from lib.io.reporting			import reporting_init,timestamp_log
from lib.io.util				import *
from lib.options				import *
from lib.interfaces.model_utils import unpickle_model


def evaluate(threadfile, model, extractor, window_size = 1, bandwidth = 1000000, LAG_TIME = 10, offset=0):
	posts_log, visit_log, result_log = timestamp_log(
			'posts',
			'visit',
			'sliding_window')
	try:
		time = 0
		d_visit = LAG_TIME
		time_visit = time
		time_visit += d_visit
		post_buffer = []
		visits = 0
		
		visit_times = []
		posts_times = []
		for window,d_t in windowed([threadfile],window_size,offset):

			#post being made
			print "%d\t-->"%time
			posts_log.write("%d\n"%time)
			posts_times.append(time)

			assert(time_visit - time > 0)

			time_post = time + d_t
			post_buffer.append(window)

			last_post_time = time
			while time_visit <= time_post:
				#visit being made
				time = time_visit
				print "%d\t<--"%time
				visits += 1
				visit_log.write("%d\n"%time)
				visit_times.append(time)
				
				if post_buffer:
					feature_vec = extractor.extract(post_buffer[-1])
					d_visit = model.predict(feature_vec,d_t)
					post_buffer = []
				else:
					d_visit = model.repredict()

				p_from_last_post     = last_post_time + d_visit

				if   time < p_from_last_post:
					time_visit = p_from_last_post
				else:
					d_visit = model.repredict()
					time_visit = time + d_visit

			time = time_post

		k = 120
		N = int(max(visit_times[-1],posts_times[-1]))
		
		sum_Phi = 0
		sum_Psi = 0
		sum_ref = 0
		for i in range(N-k):
			r = len([j for j in posts_times if j >= i and j < i + k ])
			h = len([j for j in visit_times if j >= i and j < i + k ])
			if r > 0: sum_ref += 1
			if   r > h: sum_Phi += 1
			elif r < h: sum_Psi += 1
			
		Pr_miss = float(sum_Phi)/sum_ref
		Pr_fa   = float(sum_Psi)/float(N-k)
		
		
		Pr_error = 0.5*Pr_miss + 0.5*Pr_fa
		result_log.write(str(Pr_miss) + ' , ' + str(Pr_fa) + '\n')
		model.add_experiment('prerror_test',threadfile,Pr_error)
		model.save()

		return Pr_error,visits
	except Exception:
		raise
	finally:
		posts_log.close()
		visit_log.close()
		result_log.close()


eval_file  = None
model_name = None
extr_name  = None

class Extractor:
	def extract(self,window):
		return window[0]


if __name__ == "__main__":
	o,args = read_options()
	reporting_init(o,"reports")
	extractor   = load_from_file(o['extractor_name'], "Extractor")
	model       = load_from_file(o['model_name'],"Model",o)
	
	if o.has_key('pickled_model'):
		pickle_file = o['pickled_model']
		model = unpickle_model(open(pickle_file,'rb'))

	result =  evaluate(
					o['test_file'],
					model,
					extractor,
					pickle_file,
					o['window_size']
			)
	print result
	#for i,j in windowed(["thread"],1):print j
