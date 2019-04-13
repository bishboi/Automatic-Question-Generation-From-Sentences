import nltk
from nltk import *
with open('data.txt', 'r') as myfile:
	data = myfile.read().replace('\n', '')
#create tokenized data
text = word_tokenize(data)
#create a list yo of pos tagged tuples 
yo = nltk.pos_tag(text)
print(yo)
#define a list for new data
li = []
for x in yo:
	if x[0] == ".":
		li.append("? ")
	elif x[1] == "NN":
		li.append("what")
	else: 
		li.append(x[0] )
#printing the list
for y in li:
	print(y, end=" ")
