class SlidingWindow():
	def __init__(self,K = 60, alpha = 0.5):
		self.window = []
		self.low  = 0
		self.window_size = K
		self.alpha = alpha
		self.phi_count = 0
		self.psi_count = 0
		self.ref_count = 0
		self.all_count = 0

	def event(self,event_type,time):
		time = int(time)
		if time >= self.low + self.window_size :
			low = self.low
			for t in range(low, time - self.window_size + 1):
				#print t
				self.low = t
				#Add appropriate counts
				if self.window:
					while self.window[0][0] < self.low:
						self.window.pop(0)
						if not self.window: break
				self.count()
			self.low = t + 1
			self.window.append((time,event_type))
			#print self.low, self.window[0]
			while self.window[0][0] < self.low:
				self.window.pop(0)
				if not self.window: break
		else:
			self.window.append((time,event_type))
		#print self.window
		
	def count(self):
		R = [j for j,et in self.window if et == 'post']
		H = [j for j,et in self.window if et == 'visit']
		
		#print H, self.low + self.window_size -1
		r = len(R)
		h = len(H)
		if   r > 0: self.ref_count += 1
		if   r > h: self.phi_count += 1
		elif r < h: self.psi_count += 1
		self.all_count += 1

	def pr_error(self):
		pr_miss = float(self.phi_count)/self.ref_count
		pr_fa   = float(self.psi_count)/(self.all_count)
		pr_error = self.alpha*pr_miss + (1-self.alpha)*pr_fa

		return pr_miss, pr_fa, pr_error



if __name__ == "__main__":
	k = 10
	
	
	posts = [(t*2 ,'post')  for t in range(10)] +\
			[(t*2 ,'post')  for t in range(30,40)]
	
	visit = [(t*8+1	,'visit') for t in range(10)]
	
	sum = 0
	for i in range(len(posts)-1):
		a,b = posts[i:i+2]
		sum += b[0]-a[0]
		
	w = SlidingWindow(K =int(float(sum)*0.5/(len(posts) -1)) )
	events = posts + visit
	events.sort()
	print events[-1]
	posts_times = [i for i,_ in posts]
	visit_times = [i for i,_ in visit]
	"""
	sum_Phi = 0
	sum_Psi = 0
	sum_ref = 0
	for i in range(events[-1][0]-k + 1):
		R = [j for j in posts_times if j >= i and j < i + k ]
		H = [j for j in visit_times if j >= i and j < i + k ]
		print H, i + k - 1
		r = len(R)
		h = len(H)
		if r > 0: sum_ref += 1
		if   r > h: sum_Phi += 1
		elif r < h: sum_Psi += 1
		
	Pr_miss = float(sum_Phi)/sum_ref
	Pr_fa   = float(sum_Psi)/float(events[-1][0]-k + 1)

	
	Pr_error = 0.5*Pr_miss + 0.5*Pr_fa

	print Pr_miss,Pr_fa,Pr_error
	"""

	for t,e in events: w.event(e,t)
	print w.pr_error()
	

	

