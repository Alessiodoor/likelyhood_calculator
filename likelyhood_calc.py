from numpy import random
import csv
import os
import glob

class Node:
	def __init__(self, header): 
		#print(header)
		self.header = header
		self.cpt = {}
	
	def add_Row(self,row):
		chiave = ""
		if((len(row)-1) == 0):
			chiave = "T"
		for a in range(0, len(row)-1):
			chiave = chiave + row[a]
		self.cpt[chiave] = float(row[len(row)-1]) 

	def get_prob(self, key):
		return self.cpt[key]

	def have_parents(self):
		return len(self.header) > 0

	def get_parents(self):
		return self.header

def binary_sampling(nodename, probability):
	probabilities = []
	probabilities.append(probability)
	probabilities.append(1 - probabilities[0])
	realization = []
	if probabilities[0] <= 0.5:
		realization.append('F')
		realization.append('T')
	else:
		realization.append('T')
		realization.append('F')
	probabilities.sort(reverse = True)
	cumulate = []
	cumulate.append(probabilities[0])
	cumulate.append(cumulate[0] + probabilities[1])
	v = random.rand()

	if v <= cumulate[0]:
		return realization[0]
	else:
		return realization[1]

def generate_samples(ord_top, evidences, nodes, n_samples):
	samples = []
	for i in range(0, n_samples):
		sample = {}
		for node in ord_top:
			if(node in evidences.keys()):#evidenziato
				sample[node] = evidences[node]
			else:
				if nodes[node].have_parents():
					chiave = ''
					for par in nodes[node].get_parents():
						chiave = chiave + sample[par]

					#print(chiave)
					sample[node] = binary_sampling(node, nodes[node].get_prob(chiave))
				else:
					sample[node] = binary_sampling(node, nodes[node].get_prob('T'))
		samples.append(sample)

	return samples

def weighted_sample(evidences, nodes, sample):
	w = 1
	for node in evidences:
		if nodes[node].have_parents():
			chiave = ''
			for par in nodes[node].get_parents():
				chiave = chiave + sample[par]
		else:
			chiave = 'T'

		prob = nodes[node].get_prob(chiave)
		if sample[node] == 'F':
			prob = 1 - prob

		w = w * prob

	return w

def likelihood_weighting(evidences, nodes, samples, query):
	w_total = 0
	w_query = 0
	for sample in samples:
		w = weighted_sample(evidences, nodes, sample)
		w_total = w_total + w
		if sample[query[0]] == query[1]:
			w_query = w_query + w

	return w_query/w_total

#main
ord_top = ["H","W","A","J"]
dizionarioNodi = {}
	
for x in ord_top:
	filename = x + ".csv"
	with open(filename) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		#Node(csv_reader.rows())
		header = next(csv_reader)

		header.remove('T')

		a = Node(header)
		for row in csv_reader:	
			a.add_Row(row)
		dizionarioNodi[x] = a		

#set evidance
evidences = {}
evidences['A'] = 'T'
query = ('J', 'T')

#generate samples
samples = generate_samples(ord_top, evidences, dizionarioNodi, 1000)
#calculate probability
prob = likelihood_weighting(evidences, dizionarioNodi, samples, query)

print(round(prob, 5))