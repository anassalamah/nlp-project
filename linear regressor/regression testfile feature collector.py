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

joined_data_file_name = "../answer combiner/test Combined Scores.csv"
joined_data = DictReader(open(joined_data_file_name, 'r'))

test_file_name = "../csv/test.csv"
test_data = DictReader(open(test_file_name, 'r'))
Q_score_dict = defaultdict(float)
IR_score_dict = defaultdict(float)
sent_pos_dict = defaultdict(int)
category_dict = defaultdict(str)
for ii in test_data:
    Q_dict = guess_score_dict(ii['QANTA Scores'])
    for key in Q_dict.keys():
        Q_score_dict[(ii['Question ID'],key)] = Q_dict[key]
    IR_dict = guess_score_dict(ii['IR_Wiki Scores'])
    for key in IR_dict.keys():
        IR_score_dict[(ii['Question ID'],key)] = IR_dict[key]
    category_dict[ii['Question ID']] = ii['category']
    sent_pos_dict[ii['Question ID']] = ii['Sentence Position'] # question len
    


outfile_name = "features_test.csv"
    
if WRITE_FILE:
    # Create File for combined scores
    outfile = open(outfile_name, 'w')
    #o = DictWriter(outfile, ['Question ID','Scores'], lineterminator='\n')
    o = DictWriter(outfile, ['Question ID','Sentence Position','Answer','Q score','IR score','join score','category'], lineterminator='\n')
    o.writeheader()

num_examples = 0

for ii in joined_data:

    """
    Question ID
    Sentence Position
    Scores
    """

    Q_ID = ii['Question ID']
    join_d = guess_score_dict(ii['Scores'])

    for guess in join_d.keys():
        num_examples += 1
        join_score = join_d[guess]
        Q_score = Q_score_dict[(Q_ID,guess)]
        IR_score = IR_score_dict[(Q_ID,guess)]
        sent_pos = sent_pos_dict[Q_ID]
        category = category_dict[Q_ID]
    
        if WRITE_FILE:
            o.writerow({'Question ID': Q_ID, \
                        'Sentence Position': sent_pos, \
                        'Answer': guess, \
                        'Q score': Q_score, \
                        'IR score': IR_score, \
                        'join score': join_score, \
                        'category': category})


if WRITE_FILE:
    print "wrote", num_examples, "lines"
    outfile.close()
else:
    print "DONE"
