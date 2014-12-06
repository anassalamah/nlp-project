from collections import defaultdict
from collections import Counter
from csv import DictReader, DictWriter

import nltk

import re

def find_links(text):
    links = re.findall("[a-z'.]+_[.\(\)a-z'_]+^.", text)
    return links

def guess_list(guesses):
    keys = []
    for jj in guesses.split(", "):
        key, val = jj.split(":")
        keys += [key.strip()]
    return keys


""" train fields:
Question ID,
Question Text,
QANTA Scores,
Answer,
Sentence Position,
IR_Wiki Scores,
category
"""

""" test fields:
Question ID,
Question Text,
QANTA Scores,
Sentence Position,
IR_Wiki Scores,
category
"""



debug = 0

if __name__ == "__main__":

    # Counter() is like defaultdict()
    all_link_dict = Counter()
    Q_link_dict = Counter()
    IR_link_dict = Counter()
    test_link_dict = Counter()
    train_link_dict = Counter()

    #print "read training data"
    train = DictReader(open("../train.csv", 'r'))

    train_examples = 0
    
    for ii in train:
        train_examples += 1
                    
        #links = find_links(ii['QANTA Scores'])
        links = guess_list(ii['QANTA Scores'])
        for jj in links:
            #print jj
            all_link_dict[jj] += 1
            Q_link_dict[jj] += 1
            train_link_dict[jj] += 1
            
        #links = find_links(ii['IR_Wiki Scores'])
        links = guess_list(ii['IR_Wiki Scores'])
        for jj in links:
            #print jj
            all_link_dict[jj] += 1
            IR_link_dict[jj] += 1
            train_link_dict[jj] += 1
            
        #raw_input()

    #print "read testing data"            
    test = DictReader(open("../test.csv", 'r'))

    test_examples = 0

    for ii in test:
        test_examples += 1
        
        # actually want to get all the words
        links = find_links(ii['QANTA Scores'])
        for jj in links:
            #print jj
            all_link_dict[jj] += 1
            Q_link_dict[jj] += 1
            test_link_dict[jj] += 1
            
        # actually want to get all the words
        links = find_links(ii['IR_Wiki Scores'])
        for jj in links:
            #print jj
            all_link_dict[jj] += 1
            IR_link_dict[jj] += 1
            test_link_dict[jj] += 1
            
    # Create File for writing
    o = DictWriter(open('wiki_links.csv', 'w'), ['link','allcount','QANTA','IR_Wiki','train','test'], lineterminator='\n')
    o.writeheader()

    # if want to get rid of underscores: key_spaced = replace(key,"_"," ")
 
    for key in all_link_dict.keys():    
        o.writerow({'link': key, \
                    'allcount': all_link_dict[key], \
                    'QANTA': Q_link_dict[key], \
                    'IR_Wiki': IR_link_dict[key], \
                    'train': train_link_dict[key], \
                    'test': test_link_dict[key], \
                    })

    print "DONE"
