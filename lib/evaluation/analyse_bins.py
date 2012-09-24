import sys,operator
import shelve
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import bsddb3

from collections import defaultdict

K = int(sys.argv[1])
output_file = sys.argv[2]
transit_file = sys.argv[3]
bins = shelve.BsdDbShelf(bsddb3.hashopen('bins.data', 'r'))
#bins = shelve.open('bins.data','r')


out = open(output_file,'w')
keys = [int(key) for key in bins]
keys.sort()

for key in keys:
	key = str(key)
	print "Evaluating ",key, " ..."
	sorted_top = sorted(
			bins[key].iteritems(),
			key=operator.itemgetter(1),
			reverse = True)[:K]
	total = sum(v for _,v in sorted_top)
	sorted_top = map(lambda tup: (tup[0],float(tup[1])/total), sorted_top)
	out.write('%10d\t'%(20*int(key)))
	out.write('\t'.join('%10s'  %i 	for i,_ in sorted_top) + '\n')
	out.write('%10s\t'%"")
	out.write('\t'.join('%10.5f'%i	for _,i in sorted_top) + '\n')
out.close()
bins.close()

states = set()
#time_trans = shelve.open('trans_bins.data','r')
time_trans = shelve.BsdDbShelf(bsddb3.hashopen('trans_bins.data', 'r'))
state_total = defaultdict(int)
transited_to = set()
transited_from = set()
for key in time_trans:
	p,n = [int(i) for i in key.split('-')]
	transited_to.add(n)
	transited_from.add(p)

transited_to   = sorted(list(transited_to))
transited_from = sorted(list(transited_from))

for i in transited_from: state_total[i] = sum(time_trans.get("%d-%d"%(i,j),0) for j in transited_to)

"""
out=open(transit_file,'w')
out.write('\t'.join("%5s"%j for j in transited_to)+ '\n')
for i in transited_from:
	out.write('\t'.join("%5.4f"%(time_trans.get("%d-%d"%(i,j),0)/float(state_total[i]))for j in transited_to)+ '\n')
out.close()
"""

def pdensity(dimI,dimJ):
	print "Creating sparse matrix %d,%d"%(dimI,dimJ)
	#pd = lil_matrix((dimI,dimJ),dtype=np.float32)
	pd = np.zeros((dimI,dimJ),dtype=np.float32)
	for key in time_trans:
		i,j = [int(i) for i in key.split('-')]
		if i > dimI or j > dimJ: continue
		pd[i-1,j-1] = time_trans[key]/float(state_total[i])
	return pd
# make these smaller to increase the resolution

#x = arange(0, transited_from[-1], 1)
#y = arange(0, transited_to[-1],   1)
print "Constructing density matrix..."
#Z = pdensity(transited_from[-1], transited_to[-1])
Z = pdensity(100, 100)
fig = plt.figure()
#plt.imshow(Z.toarray(),cmap=cm.Greys)
im = plt.imshow(Z,cmap=cm.Greys,interpolation='nearest')

#im.set_interpolation('bicubic')
#ax.set_image_extent(-3, 3, -3, 3)
#plt.axis([0,200*20, 0, 200*20])
#fig.savefig('collated/%s'%output)
plt.title("Density matrix plot of $p(q_{t+1}|q_t)$")

plt.xlabel("$q_{t+1}$ (20 minute blocks)")
plt.ylabel("$q_{t}$ (20 minute blocks)")
plt.show()

