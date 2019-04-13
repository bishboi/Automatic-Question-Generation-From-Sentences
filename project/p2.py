import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
from pprint import pprint
nlp = en_core_web_sm.load()
with open('data.txt', 'r') as myfile:
	text = myfile.read().replace('\n', '')
doc = nlp(text)
print(text)
pprint([(X.text, X.label_) for X in doc.ents])
