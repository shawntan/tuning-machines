#!/usr/bin/python2
import nltk,re
from nltk.stem.porter import PorterStemmer
import sys,time

bin_size = 10
users = set()

def text_tdelta(input_file):
	prev_tup = None
	for line in open(input_file):
		tup = line.split('\t')
		if prev_tup: yield (
				(float(tup[0])-float(prev_tup[0]))/60,
				tup[1].strip(),
				tup[2].strip(),
				time.localtime(float(tup[0]))
				)
		prev_tup = tup


def class_text(threadfiles):
	for threadfile in threadfiles:
		for line in open(threadfile):
			tup = line.split('\t')
			users.add(tup[1])

	for threadfile in threadfiles:
		for td,text,t in text_tdelta(threadfile):
			yield (td,text,t)


def windowed(threadfiles,N, offset = -1):
	count = 0
	for threadfile in threadfiles:
		window = [None]
		prev_window = None
		for tup in text_tdelta(threadfile):
			window.append(tup)
			if prev_window: 
				if count <= offset:
					count += 1
				else:yield prev_window,tup[0]
			if len(window) > N:
				window.pop(0)
				result = [None]*len(tup)
				for i in range(len(tup)): result[i] = [t[i] for t in window]
				prev_window = tuple(result)

def filter_tokenise(text):
	r = []
	for w in text.split():
		w = preprocess(w)
		if w: r.append(w)
	return r


non_alphanum = re.compile('\W') 
number = re.compile('[0-9]')
splitter = re.compile('[\s\.\-\/]+')
stemmer = PorterStemmer()
stop_words = set(nltk.corpus.stopwords.words('english'))
def preprocess(word):
	global users
	w = non_alphanum.sub("",word)
	w = w.lower()
	if w in stop_words: return
	if w in users: return "#USER#"
	w = stemmer.stem_word(w)
	w = number.sub("#",w)
	return w
