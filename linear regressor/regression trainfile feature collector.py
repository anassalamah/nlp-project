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
answer_key_dict = defaultdict(str)
for ii in key_data:
    answer_key_dict[(ii['Question ID'],ii['Sentence Position'])] = ii['Answer']

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
num_right_examples = 0
num_wrong_examples = 0


key_data = DictReader(open(key_file_name, 'r'))
input_num = 0
for ii in key_data:
    input_num += 1
    num_questions += 1
    # split the answer fields into seperate anwers
    Q_d = guess_score_dict(ii['QANTA Scores'])
    IR_d = guess_score_dict(ii['IR_Wiki Scores'])

    #if len(Q_d) > 20 or len(IR_d) > 20:
    #    print "BIG LEN", ii['Question ID'], "Q#", len(Q_d), "IR#", len(IR_d)


    Q_ID = (ii['Question ID'],ii['Sentence Position'])

    # collect the features of the known answer:    
    right_guess = answer_key_dict[Q_ID]
    Q_score = Q_d[right_guess]
    IR_score = IR_d[right_guess]

    if WRITE_FILE:
        num_examples += 1
        num_right_examples += 1
        o.writerow({'Question ID': ii['Question ID'], \
                    'Sentence Position': ii['Sentence Position'], \
                    'Answer': right_guess, \
                    'is correct': 1, \
                    'Q score': Q_score, \
                    'IR score': IR_score, \
                    'join score': joined_data_dict[(ii['Question ID'],ii['Sentence Position'],right_guess)], \
                    'category': ii['category']})


    # collect the features of known wrong answers:
    known_answer = answer_key_dict[Q_ID]
    bad_guess_list = []
    for key in Q_d.keys():
        if key != known_answer:
            if key not in bad_guess_list:
                bad_guess_list = bad_guess_list + [key]
    for key in IR_d.keys()[:20]:
        if key != known_answer:
            if key not in bad_guess_list:
                bad_guess_list = bad_guess_list + [key]

    bad_guess_dict = defaultdict(int)
    for key in Q_d.keys():
        if key != known_answer:
            bad_guess_dict[key] += 1
    for key in IR_d.keys()[:20]:
        if key != known_answer:
            bad_guess_dict[key] += 1

    key_tally = 0
    for key in bad_guess_dict:
        key_tally += 1

    if key_tally > 40:
        print "thislen", key_tally
    
    if len(bad_guess_list) > 40:
        print "bad len", len(bad_guess_list)

    #for guess in bad_guess_list[:NUM_BAD_ANSWERS]:
    for guess in bad_guess_list:
        Q_score = Q_d[guess]
        IR_score = IR_d[guess]

        if WRITE_FILE:
            num_examples += 1
            num_wrong_examples += 1
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
    print "wrote", num_right_examples, "correct examples"
    print "wrote", num_wrong_examples, "wrong examples"
    outfile.close()
else:
    print "DONE"
