import nltk.classify.maxent
from nltk.classify.maxent import MaxentClassifier
# C:\Python27\lib\site-packages\nltk\classify\maxent.py
from nltk.classify.util import accuracy 
# C:\Python27\lib\site-packages\nltk\classify\util.py

from csv import DictReader, DictWriter
from collections import defaultdict

# for names_demo:
from nltk.corpus import names
import random

# VARIABLES:
WRITE_FILE = 0
USE_TRAIN_DATA = 1

def feature_finder(name):
    features = {}
    #features['alwayson'] = True
    features['startswith'] = name[0].lower()
    features['endswith'] = name[-1].lower()
    #for letter in 'abcdefghijklmnopqrstuvwxyz':
    #    features['count(%s)' % letter] = name.lower().count(letter)
    #    features['has(%s)' % letter] = letter in name.lower()
    return features

def guess_score_dict(guesses):
    """
    returns a dictionary of ([guess] = value) of all guess
    """
    d = defaultdict(float)
    for jj in guesses.split(", "):
        key, val = jj.split(":")
        d[key.strip()] = float(val)
    
    return d


## BEGIN ##

if USE_TRAIN_DATA:
    key_file_name = "../csv/train.csv"
    key_data = DictReader(open(key_file_name, 'r'))

    outfile_name = "features_DEV_train.csv"
    

else:
    outfile_name = "features_DEV_test.csv"

# generate an answer key dictionary
key_dict = defaultdict(str)
for ii in key_data:
    key_dict[(ii['Question ID'],ii['Sentence Position'])] = ii['Answer']

if WRITE_FILE:
    # Create File for combined scores
    outfile = open(outfile_name, 'w')
    #o = DictWriter(outfile, ['Question ID','Scores'], lineterminator='\n')
    o = DictWriter(outfile, ['Question ID','Sentence Position','Answer','is correct','Q score','IR score'], lineterminator='\n')
    o.writeheader()

num_examples = 0

key_data = DictReader(open(key_file_name, 'r'))
input_num = 0
for ii in key_data:
    input_num += 1
    if input_num % 3 == 0:
        # split the answer fields into seperate anwers
        Q_d = guess_score_dict(ii['QANTA Scores'])
        IR_d = guess_score_dict(ii['IR_Wiki Scores'])

        #join_d = defaultdict(float)
        #for key in Q_d.keys():
        #    join_d[key] = 1
        #for key in IR_d.keys():
        #    join_d[key] = 1

        Q_ID = (ii['Question ID'],ii['Sentence Position'])

        # collect the features of the known answer:
        num_examples += 1
        guess = key_dict[Q_ID]
        Q_score = Q_d[guess]
        IR_score = IR_d[guess]

        if WRITE_FILE:
            o.writerow({'Question ID': ii['Question ID'], \
                        'Sentence Position': ii['Sentence Position'], \
                        'Answer': guess, \
                        'is correct': 1, \
                        'Q score': Q_score, \
                        'IR score': IR_score})


        # collect the features of a known wrong answer:
        num_examples += 1
        for key in Q_d.keys():
            if key != key_dict[Q_ID]:
                guess = key
                break
        Q_score = Q_d[guess]
        IR_score = IR_d[guess]

        if WRITE_FILE:
            o.writerow({'Question ID': ii['Question ID'], \
                        'Sentence Position': ii['Sentence Position'], \
                        'Answer': guess, \
                        'is correct': 0, \
                        'Q score': Q_score, \
                        'IR score': IR_score})
            
        
    
if WRITE_FILE:
    print "wrote", num_examples, "lines"
    outfile.close()
else:
    print "DONE"
