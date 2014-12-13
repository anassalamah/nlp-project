import nltk.classify.maxent
from nltk.classify.maxent import MaxentClassifier
# C:\Python27\lib\site-packages\nltk\classify\maxent.py
from nltk.classify.util import accuracy 
# C:\Python27\lib\site-packages\nltk\classify\util.py

from csv import DictReader, DictWriter
from collections import defaultdict

from random import shuffle

# VARIABLES:
WRITE_FILE = 1

# number of questions to include in training set:
COLLECT_ONE_OUT_OF = 1 

# number of wrong answers for each question to include:
NUM_BAD_ANSWERS = 100

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

key_file_name = "../csv/train.csv"
key_data = DictReader(open(key_file_name, 'r'))

outfile_name = "features_train.csv"

# generate an answer key dictionary
key_dict = defaultdict(str)
for ii in key_data:
    key_dict[(ii['Question ID'],ii['Sentence Position'])] = ii['Answer']

if WRITE_FILE:
    # Create File for combined scores
    outfile = open(outfile_name, 'w')
    #o = DictWriter(outfile, ['Question ID','Scores'], lineterminator='\n')
    o = DictWriter(outfile, ['Question ID','Sentence Position','Answer','is correct','Q score','IR score','join score','category'], lineterminator='\n')
    o.writeheader()

joined_data_file_name = "../answer combiner/train Combined Scores.csv"
joined_data = DictReader(open(joined_data_file_name, 'r'))
joined_data_dict = defaultdict(float)
for ii in joined_data:
    join_d = guess_score_dict(ii['Scores'])
    for key in join_d.keys():
        joined_data_dict[(ii['Question ID'],ii['Sentence Position'],key)] = join_d[key]


num_examples = 0
num_questions = 0
key_data = DictReader(open(key_file_name, 'r'))
input_num = 0
for ii in key_data:
    input_num += 1
    #if input_num % 3 == 0:
    #if int(ii['Question ID']) % 3 == 0:
    if input_num % COLLECT_ONE_OUT_OF == 0:
        num_questions += 1
        # split the answer fields into seperate anwers
        Q_d = guess_score_dict(ii['QANTA Scores'])
        IR_d = guess_score_dict(ii['IR_Wiki Scores'])

        Q_ID = (ii['Question ID'],ii['Sentence Position'])

        # collect the features of the known answer:
        
        guess = key_dict[Q_ID]
        Q_score = Q_d[guess]
        IR_score = IR_d[guess]

        if WRITE_FILE:
            num_examples += 1
            o.writerow({'Question ID': ii['Question ID'], \
                        'Sentence Position': ii['Sentence Position'], \
                        'Answer': guess, \
                        'is correct': 1, \
                        'Q score': Q_score, \
                        'IR score': IR_score, \
                        'join score': joined_data_dict[(ii['Question ID'],ii['Sentence Position'],guess)], \
                        'category': ii['category']})


        # collect the features of a known wrong answer:
        known_answer = key_dict[Q_ID]
        bad_guess_list = []
        for key in Q_d.keys():
            if key != known_answer:
                bad_guess_list = bad_guess_list + [key]
        for key in IR_d.keys():
            if key != known_answer:
                if key not in bad_guess_list:
                    bad_guess_list = bad_guess_list + [key]

        shuffle(bad_guess_list)
    
        for guess in bad_guess_list[:NUM_BAD_ANSWERS]:
            num_examples += 1
            Q_score = Q_d[guess]
            IR_score = IR_d[guess]

            if WRITE_FILE:
                o.writerow({'Question ID': ii['Question ID'], \
                            'Sentence Position': ii['Sentence Position'], \
                            'Answer': guess, \
                            'is correct': 0, \
                            'Q score': Q_score, \
                            'IR score': IR_score, \
                            'join score': joined_data_dict[(ii['Question ID'],ii['Sentence Position'],guess)], \
                            'category': ii['category']})

                
if WRITE_FILE:
    print "used", num_questions, "questions"
    print "wrote", num_examples, "lines"
    outfile.close()
else:
    print "DONE"
