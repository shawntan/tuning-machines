import math

class PairwiseScoring():
	def __init__(self,scoring = {
		('visit','visit') : lambda e1,e2:   math.exp(0.01*(e1-e2)),
		('post', 'visit') : lambda e1,e2: 1-math.exp(0.01*(e1-e2)),
		('post', 'post' ) : lambda e1,e2: 0						,
		('visit','post' ) : lambda e1,e2: 0}):
		self.total_score = 0
		self.count = 0
		self.prev_event = (None,0)
		self.scoring = scoring

	def event(self,event_type,time):
		if self.prev_event[0]:
			et1,et2 = self.prev_event[0],event_type
			t1,t2   = self.prev_event[1],time
			score = self.scoring[et1,et2](float(t1),float(t2))
			#print "%10s\t%10s\t%10d\t%10d\t%10.10f"%(et1,et2,t1,t2,score)
			if score > 0 : self.count += 1
			self.total_score += score
		self.prev_event = (event_type,time)
		
	def score(self):
		return self.total_score/self.count




if __name__ == "__main__":
	k = 10
	
	posts = [(t*10 ,'post')  for t in range(10)] +\
			[(t*10 ,'post')  for t in range(30,40)]
	
	visit = [(t+13 ,'visit') for t,_ in posts]
	
	sum = 0
	for i in range(len(posts)-1):
		a,b = posts[i:i+2]
		sum += b[0]-a[0]
		
	events = posts + visit
	events.sort()
	posts_times = [i for i,_ in posts]
	visit_times = [i for i,_ in visit]
	
	w = PairwiseScoring()

	for t,e in events: w.event(e,t)
	print w.score()
	

	

