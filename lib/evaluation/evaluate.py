#!/usr/bin/python2

from lib.io.reader				import windowed
from lib.io.reporting			import reporting_init,timestamp_log
from lib.io.util				import *
from lib.options				import *
from lib.interfaces.model_utils import unpickle_model

from lib.evaluation.sliding_window	import SlidingWindow
from lib.evaluation.pairwise		import PairwiseScoring

def evaluate(threadfile, model, extractor,
			window_size = 1,
			bandwidth = 1000000,
			LAG_TIME = 10,
			offset = 0,
			sliding_window_size = 120,
			verbose = False
			):
	posts_log, visit_log, result_log_tscore,result_log_window = timestamp_log(
			'posts',
			'visit',
			't_score',
			'sliding_window')
	try:
		time = 0
		d_visit = LAG_TIME
		time_visit = time
		time_visit += d_visit
		post_buffer = []
		
		t_score_cum = 0
		count = 0
		visits = 0
		

		correct_count,wrong_count = 0,0
		w = SlidingWindow(K = 20, alpha = 0.5)
		ps = PairwiseScoring()
		for window,d_t in windowed([threadfile],window_size, offset):
			#post being made
			if verbose: print "%d\t-->"%time
			posts_log.write("%d\n"%time)
			w.event('post',time)
			ps.event('post',time)

			assert(time_visit - time > 0)
			t_score_cum += time_visit-time
			count += 1
			time_post = time + d_t
			post_buffer.append((extractor.extract(window),d_t))

			last_post_time = time
			
			
			while time_visit <= time_post:
				#visit being made
				time = time_visit
				if verbose: print "%d\t<--"%time
				visits += 1
				visit_log.write("%d\n"%time)
				w.event('visit',time)
				ps.event('visit',time)
				#start correction
				d_visit = None
				if post_buffer: feature_vec,_ = post_buffer[-1]
				d_visit = model.predict(
						feature_vec,d_t,
						current_d_t = time - last_post_time,
						unseen = post_buffer[:-1]
				)

				if post_buffer: post_buffer = []
				time_visit = last_post_time + d_visit
				
				assert(time < time_visit)
				
				#end correction
			time = time_post

		Pr_miss, Pr_fa, Pr_error = w.pr_error()
		result_log_window.write(str(Pr_miss) + ' , ' + str(Pr_fa) + '\n')
		model.add_experiment('prerror_test',threadfile,Pr_error)
		model.add_experiment('pairwise_scoring',threadfile,ps.score())

		t_score = t_score_cum/float(count)
		result_log_tscore.write(str(t_score)+'\n')
		model.add_experiment('t-score_test',threadfile,t_score)
		#save_model(pickle_file,model)
		model.save()

		return {
			'T-score':  t_score,
			'Pr_error': (Pr_miss,Pr_fa,Pr_error),
			'Visits':   visits,
			'Posts':    count,
			'Pairwise': ps.score()
			#'Invalid Predictions': (correct_count+wrong_count,
							#	wrong_count/float(correct_count+wrong_count))
			}
	except Exception:
		raise
	finally:
		posts_log.close()
		visit_log.close()
		result_log_tscore.close()
		result_log_window.close()


if __name__ == "__main__":
	o,args = read_options()
	reporting_init(o,"reports")
	extractor   = load_from_file(o.extractor_name, "Extractor")
	model       = load_from_file(o.model_name,"Model",o)
	
	if o.pickled_model:
		pickle_file = o.pickled_model
		model = unpickle_model(open(pickle_file,'rb'))

	result =  evaluate(
					o.test_file,
					model,
					extractor,
					o.window_size,
					verbose = o.verbose
			)
	#print result
	#for i,j in windowed(["thread"],1):print j
