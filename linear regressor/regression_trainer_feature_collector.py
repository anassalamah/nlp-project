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
WRITE_FILE = 1
USE_TRAIN_DATA = 1

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
    #if input_num % 3 == 0:
    if int(ii['Question ID']) % 3 == 0:
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
        bad_guess_list = []
        for key in Q_d.keys()[:3]:
            if key != key_dict[Q_ID]:
                bad_guess_list += [key]
        for key in IR_d.keys()[:3]:
            if key != key_dict[Q_ID]:
                if key not in bad_guess_list:
                    bad_guess_list += [key]
    
        for guess in bad_guess_list:
            num_examples += 1
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
