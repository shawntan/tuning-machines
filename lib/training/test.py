import lda
from utils.reader import windowed,filter_tokenise
import sys
import matplotlib.pyplot as plt
from collections import defaultdict
def plot_hist(bin_size,bin_list, upper =None):
	for bins in bin_list:
		fig = plt.figure()
		ax = fig.add_subplot(1,1,1)
		up_bound = upper or max(bins)
		x = [i for i in range(up_bound+1)]
		y = [bins[i] for i in range(up_bound+1)]
#		print x
#		print y
		ax.bar(x,y,width=1)
		plt.show()


docs = [' '.join(w[2]) for w,_ in windowed(sys.argv[2:],int(sys.argv[1]))]
tokenised_docs = [filter_tokenise(i) for i in docs]
num_topics = 3
lda = lda.LDASampler(
	docs=tokenised_docs,
	num_topics=num_topics, 
	alpha=0.25,
	beta=0.25)

print 'Sampling...'
for _ in range(100):
	zs = lda.assignments
	#print zs
	#print '[%i %i] [%i %i]' % (zs[0][3], zs[1][3], zs[2][3], zs[3][3])
	lda.next()
print

print 'words ordered by probability for each topic:'
tks = lda.topic_keys()
for i, tk in enumerate(tks):
	print '%3d'%i , tk[:10]
#	print '%3s'%'', tk[10:20]
#	print '%3s'%'', tk[20:30]
print

print 'document keys:'
dks = lda.doc_keys()
size = 20
time_differences = [dt for _,dt in windowed(sys.argv[2:],int(sys.argv[1]))]

bin_list = []
for i in range(num_topics):
	bins = defaultdict(float)
	bin_list.append(bins)

for dt, doc, dk in zip(time_differences, docs, dks):
	print '%5d'%dt + '\t'+\
		  doc[:40] +"..." + '\t' +\
		  str(dk)
	for p,i in dk:
		bin = int(float(dt)/size)
		bin_list[i][bin] += p

plot_hist(size,bin_list)
#print 'topic assigned to each word of first document in the final iteration:'
#lda.doc_detail(0)
