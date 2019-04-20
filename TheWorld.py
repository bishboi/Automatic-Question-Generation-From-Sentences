import nltk
from nltk.tree import Tree
from nltk import * 
from nltk.corpus import wordnet as wn
from nltk.tree import ParentedTree
def readfrom(location):
	'''
	Hello this function is defined for reading the input file into the string
	'''		
	with open(location, 'r') as myfile:
		corpus = myfile.read().replace('\n', '')
	return corpus

def stanfordparser(corpus):
	'''
	Hello this funtion is defined for web scraping for stanford Parser
	'''
	from selenium import webdriver
	from selenium.webdriver.support.ui import Select
	from selenium.webdriver.common.keys import Keys
	#Setting up URL
	nlp = "http://nlp.stanford.edu:8080/parser/"
	#Setting up Driver
	driver = webdriver.Firefox()
	#initializing URL
	driver.get(nlp)
	#Finding text area
	text_area = driver.find_element_by_name("query")
        #clearing the pre written text
	text_area.clear()
	#enetering thext
	text_area.send_keys(corpus)
	#Clicking on submit
	driver.find_element_by_name("parse").click()
	#Getting element with output, stored under pre tag
	text = driver.find_elements_by_id("parse")
	#taking element from list and converting it in string
	for x in text:
		data = x.text
	#close
	driver.close()
	parsetree = Tree.fromstring(data)
	#nltk tree format
	return parsetree

tree = stanfordparser(readfrom('Data/data.txt'))
parsetree = ParentedTree.convert(tree)
withoutSBAR = ParentedTree.convert(tree)
def eraseSBAR(tree,full):
    '''
    Hello this function traverse the tree recursively and it deletes the SBAR subtree
    '''
    for subtree in tree:
        if type(subtree) == nltk.tree.ParentedTree:
            if subtree.label() == 'SBAR':
                full[subtree.treeposition()]=''
                return full
            eraseSBAR(subtree,full)
    return full

withoutSBAR = eraseSBAR(withoutSBAR,withoutSBAR)
questions = []
for word in parsetree.leaves():
    leaf_index = parsetree.leaves().index(word)
    tree_location = parsetree.leaf_treeposition(leaf_index)
#    print(tree_location)
#    print(parsetree[tree_location])
#    print(parsetree[tree_location[:-1]])
#    if parsetree[tree_location[:-1]].label() == 'NP':
#	 print('NP')
#    print(parsetree[tree_location[:-1]])
#    print(tree_location[:-2])
    '''
    Rule1:- possesive pronouns replaced by 'Whoes'
    '''
    if parsetree[tree_location[:-1]].label() == 'PRP$':
    	x = parsetree[tree_location[:-1]]
    	parsetree[tree_location[:-1]] = 'whoes'
    	questions.append(parsetree.leaves())
    	parsetree[tree_location[:-1]] = x
    '''
    Rule2:- pronouns other that it replaced by who
    Rule3:- it replaced by what
    '''
    if parsetree[tree_location[:-1]].label() == 'PRP':
    	if word != 'it':
    	    x = parsetree[tree_location[:-1]]
    	    parsetree[tree_location[:-1]] = 'who'
    	    questions.append(parsetree.leaves())
    	    parsetree[tree_location[:-1]] = x
    	else:
    	    x = parsetree[tree_location[:-1]]
    	    parsetree[tree_location[:-1]] = 'what'
    	    questions.append(parsetree.leaves())
    	    parsetree[tree_location[:-1]] = x

    '''
    Rule4:- smallest NP with person or animal attribute are replaced by 'Who'
    '''
    if parsetree[tree_location[:-2]].label() == 'NP':
        for synset in wn.synsets(word):
            if 'noun.person' in synset.lexname() or 'noun.animal' in synset.lexname():
                '''
                Rule5:- if smallest NP with person or animal attribute is in verb phrase then replaced by whom
                '''
                if parsetree[tree_location[:-3]].label() == 'VP':
                    x = parsetree[tree_location[:-2]]
                    parsetree[tree_location[:-2]] = 'whom'
                    questions.append(parsetree.leaves())
                    parsetree[tree_location[:-2]] = x
                else:	
                    x = parsetree[tree_location[:-2]]
                    parsetree[tree_location[:-2]] = 'who'
                    questions.append(parsetree.leaves())
                    parsetree[tree_location[:-2]] = x
            break  
        #print(parsetree[tree_location[:-2]])
        #print(tree_location[:-2])
for word in withoutSBAR.leaves():
    leaf_index = withoutSBAR.leaves().index(word)
    tree_location = withoutSBAR.leaf_treeposition(leaf_index)
    '''
    Rule1:- possesive pronouns replaced by 'Whoes'
    '''
    if withoutSBAR[tree_location[:-1]].label() == 'PRP$':
    	x = withoutSBAR[tree_location[:-1]]
    	withoutSBAR[tree_location[:-1]] = 'whoes'
    	questions.append(withoutSBAR.leaves())
    	withoutSBAR[tree_location[:-1]] = x

    '''
    Rule2:- pronouns other that it replaced by who
    Rule3:- it replaced by what
    '''
    if withoutSBAR[tree_location[:-1]].label() == 'PRP':
    	if word != 'it':
    	    x = withoutSBAR[tree_location[:-1]]
    	    withoutSBAR[tree_location[:-1]] = 'who'
    	    questions.append(withoutSBAR.leaves())
    	    withoutSBAR[tree_location[:-1]] = x
    	else:
    	    x = withoutSBAR[tree_location[:-1]]
    	    withoutSBAR[tree_location[:-1]] = 'what'
    	    questions.append(withoutSBAR.leaves())
    	    withoutSBAR[tree_location[:-1]] = x
    '''
    Rule4:- smallest NP are replaced by 'Who'
    '''
    if withoutSBAR[tree_location[:-2]].label() == 'NP':
        for synset in wn.synsets(word):
            if 'noun.person' in synset.lexname() or 'noun.animal' in synset.lexname():
                if parsetree[tree_location[:-3]].label() == 'VP':
                    '''
                    Rule5:- if smallest NP with person or animal attribute is in verb phrase then replaced by whom
                    '''
                    x = withoutSBAR[tree_location[:-2]]
                    withoutSBAR[tree_location[:-2]] = 'whom'
                    questions.append(withoutSBAR.leaves())
                    withoutSBAR[tree_location[:-2]] = x
                
                else:
                    x = withoutSBAR[tree_location[:-2]]
                    withoutSBAR[tree_location[:-2]] = 'who'
                    questions.append(withoutSBAR.leaves())
                    withoutSBAR[tree_location[:-2]] = x   
            break  

print('Stentence:',readfrom('Data/data.txt'))
print("Generated Questions:")
for i in questions:
	for j in i:
	   if j == '.':
	       j = '?'
	   print(j,end = ' ')
	print('')