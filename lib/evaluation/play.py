from lib.io.reporting import set_directory
from lib.io.util import  load_from_file
from lib.options import *
from lib.interfaces.model_utils import unpickle_model
import os
import glob
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot
import numpy as np

def plot(values,output,
		x_axis = 'Values',
		y_axis = 'Frequency',
		title  = 'Histogram',
		range_min = None,
		range_max = None):
	if range_min != None: values = [v for v in values if v >= range_min]
	if range_max != None: values = [v for v in values if v <= range_max]
	fig = pyplot.figure()
	n, bins, patches = pyplot.hist(
			values,
			60,
			facecolor = 'green',
			alpha=0.75
		)
	print n, bins, patches
	pyplot.xlabel(x_axis)
	pyplot.ylabel(y_axis)
	pyplot.title(title)
	pyplot.axis([min(values),max(values),0,max(n)])
	pyplot.grid(True)

	fig.savefig('collated/%s'%output)

def scatter_plot(x_vals,y_vals,c_vals,output,
		x_axis = 'Values',
		y_axis = 'Frequency',
		title  = 'Scatterplot'):

	fig = pyplot.figure()
	ax = fig.add_subplot(1,1,1)
	ax.set_yscale('log')
	#ax.set_xscale('log')
	pyplot.ylim((0.1,1000))
	pyplot.xlim((0,7500))
	pyplot.scatter(x_vals,y_vals,c=c_vals, cmap=mpl.cm.Greens)
	pyplot.xlabel(x_axis)
	pyplot.ylabel(y_axis)
	pyplot.title(title)
	fig.savefig('collated/%s'%output)




ws_ex = [
		#('Average $w = %d$',	 			'*w%d_winavg*',		'w%d_dt_average.result'),
		#('$w=%d,\\dtvec$',		 			'*w%d_dt-*',		'w%d_rbf_dt'),
		#('$w=%d,\\dtvec,\\ctxvec$',			'*w%d_dt_ctx*',		'w%d_rbf_dt_ctx'),
		#('$w=%d,\\vocab$',	 	'*w%d_lang-*',			'w%d_rbf_lang_fs'),
		#('$\\alpha=%0.1f,\\vocab$',	 	'*w%0.1f_lang_decay-*',	'w%0.1f_rbf_lang_fs_decay'),
		#('$w=%d,\\vocab$,p', 	'*w%d_lang_punc-*',		'w%d_rbf_lang_p_fs')
		#('$w=%d,\\vocab,\\dtvec$',			'*w%d_lang_dt-*',	'w%d_rbf_lang_dt_fs'),
		#('$w=%d,\\vocab,\\dtvec$',			'*w%d_lang_dt_decay-*',	'w%d_rbf_lang_dt_fs')
		#('cluster',	'*cluster_time-*','cluster_time')
		]

vocab_size_ex = [
		('$\\vocab,|\\vocab|=%d',	 				'*w15_lang_top%d-*',		'vocab-size%d'),
		]


patterns = []
alpha_sizes = [5,10,15,20,25,30,35,40,45,50]
for i,j,k in vocab_size_ex:
	patterns += [(i%w,j%w,k%w) for w in alpha_sizes]




if __name__ == '__main__':
	o,args = read_options()
	#extractor   = load_from_file(o['extractor_name'], "Extractor")
	for n in glob.glob('models/*.py'):
		load_from_file(n,"Model",o)
	
	summary = open('collated/summary','w')


	header_tuple = [
				'MAPE',
				'$Pr_{miss}$',
				'$Pr_{fa}$',
				'$Pr_{error}$',
				'$T$-score',
				#'Inv. pred',
				#'Posts',
				#'Visits',
				'Pairwise',
				'Visit/Post'
				]
	summary.write('%20s &\t'%'')
	summary.write(' &\t'.join("%10s"%i for i in header_tuple) + ' \\\\\n\\hline\n')

	for l_col,p,outfile in patterns:
		print 'pickled_models/'+p+'/model'
		files = glob.glob('pickled_models/'+p+'/model')
		log_file = open('collated/'+outfile,'w')
		log_file_coeffs = open('collated/'+outfile+'_coeffs','w')
		print len(files)
		
		count = 0
		sum_tup = [0]*len(header_tuple)
		log_file.write('\t'.join("%10s"%i for i in header_tuple) + '\n')


		regression_perfs = []
		t_scores         = []
		pv_ratios        = []

		tscore_pv_plot   = []
		posts_vals       = []
		for pickle_file in files:
			set_directory(os.path.dirname(pickle_file))
			model = unpickle_model(open(pickle_file,'rb'))
			print model.experiments
			for k in model.experiments:
				exps = model.experiments[k]
				values = dict((e_name,result) for e_name,_,result in exps)
				if values.has_key('visit_evaluation'):
					try:
						#print values
						regression_perf = values['regression_test(partial thread)']
						pr_miss,pr_fa,pr_error = values['visit_evaluation']['Pr_error']
						t_score = values['visit_evaluation']['T-score']
						posts = values['visit_evaluation']['Posts']
						visits = values['visit_evaluation']['Visits']
						filename = values['visit_evaluation']['filename']
						pairwise = values['visit_evaluation']['Pairwise']
						pv_ratio = visits/float(posts)
						#inv_preds = values['visit_evaluation']['Invalid Predictions'][1]
						tuple = [
								regression_perf,
								pr_miss,
								pr_fa,
								pr_error,
								t_score,
								pairwise,
								#inv_preds,
								pv_ratio
								]

						regression_perfs.append(regression_perf)
						t_scores.append(t_score)
						pv_ratios.append(pv_ratio)
						posts_vals.append(posts)

						sum_tup = [s + i for s,i in zip(sum_tup,tuple)]
						count += 1
						log_file.write('\t'.join("%10.3f"%i for i in tuple) +\
										'\t' +  filename + '\n')
					except KeyError as ke:
						print ke
				if values.has_key('token_score'):
					coeffs = values['token_score']
					log_file_coeffs.write('\t'.join("%10s"%i   for _,i in coeffs[:-1]) + '\n')
					log_file_coeffs.write('\t'.join("%10.3f"%i for i,_ in coeffs[:-1]) + '\t' +\
										"%10.3f"%coeffs[-1] + '\n')

		"""
		plot(	output = 'mape_dist_%s.png'%outfile,
				values = regression_perfs,
				x_axis = 'MAPE',
			)
		plot(	output = 't_score_dist_%s.png'%outfile,
				values = t_scores,
				x_axis = '$T$-score',
			)
		plot(	output = 'pv_ratio_dist_%s.png'%outfile,
				values = pv_ratios,
				x_axis = 'Post/Visit ratio'
			)
		"""
		scatter_plot(
				x_vals = t_scores,
				y_vals = pv_ratios,
				c_vals = posts_vals,
				x_axis = '$T$-scores',
				y_axis = 'Post/Visit ratio',
				output = 'tscore_pv_plot%s.png'%outfile,
				title  = '$T$-score vs. Post/Visit ratio'
		)

		avg_tup = [float(s)/count for s in sum_tup]
		log_file.write('\n')
		log_file.write('\t'.join("%10.3f"%i for i in avg_tup) + '\n')
		summary.write('%20s &\t'%l_col)
		summary.write(' &\t'.join("%10.3f"%i for i in avg_tup) + ' \\\\\n')

	log_file.close()
	log_file_coeffs.close()
	summary.close()
