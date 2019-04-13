import nltk
from nltk import *
import spacy
from spacy import *
import en_core_web_sm
#to take text input from myfile
with open('data.txt', 'r') as myfile:
	text = myfile.read().replace('\n', '')
#preprocess data
data = nltk.word_tokenize(text)
data = nltk.pos_tag(data)
#print(data)
#defining rule for chunking
pattern = 'NP: {<DT>?<JJ>*<NN>}'
#It process the pattern
cp = nltk.RegexpParser(pattern)
#it parse the data ie chunks it
chunked = cp.parse(data)
#print(chunked)
#lets print it in iob tagged mode for better data execution i.e one token per line
iob_tagged = tree2conlltags(chunked)
#pprint(iob_tagged)
#lets find the named entities of nltk ne_tree = named entity tree
ne_tree = ne_chunk(pos_tag(word_tokenize(text)))
print(ne_tree)
#it failed drastically
