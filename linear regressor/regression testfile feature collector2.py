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

# pronouns
person_pronouns = ['he','him','his','she','her','hers','himself','herself','each other',"each other's", 'one another', "one another's",'who','whoever','whomever','whom','whose'] 
thing_pronouns = ["it", "its"]
group_pronouns= ['they", "them", "their", theirs']
all_pronouns = person_pronouns + thing_pronouns + group_pronouns


def guess_score_dict(guesses):
    """
    returns a dictionary of ([guess] = value) of all guess
    """
    d = defaultdict(float)
    for jj in guesses.split(", "):
        key, val = jj.split(":")
        d[key.strip()] = float(val)
    
    return d

def find_pronouns(text):
    """
    find the pronouns in a question text
    """
    tokens = word_tokenize(text)
    #print tokens
    pronouns  = []
    for i in tokens:
        if i in all_pronouns:
            pronouns.append(i)
    #print pronouns
    return pronouns

def most_common_pronoun(pronouns):
    """
    return the most common pronoun,
    and in the case of many pronouns having the same count,
    return the first one that appears in the string
    """
    if pronouns:
        pronouns = max(set(pronouns), key= lambda x: (pronouns.count, -pronouns.index(x)))
        
    return pronouns

def clean_guesses(guesses, pronoun):
    """
    return a string that only has the guesses relative to its type

    """
    if not pronoun:
        print "PRONOUNS EMPTY, returning guesses as is" 
        return guesses
    elif pronoun in person_pronouns:
        # Read in person INFO
        answer_info_file = open("../csv/person_info.csv", 'r')
        answer_info = DictReader(answer_info_file)
    else:
        # Read in non_person NER
        answer_info_file = open("../csv/non_person_info.csv", 'r')
        answer_info = DictReader(answer_info_file)
    new_guesses= ""
    top_mismatch = 0
    # insert bool to know if top key matches any of the answers in the relative csv file
    found_key = False
    for jj in guesses.split(", "):
        #print jj
        key,val = jj.split(":")
        for ii in answer_info:
            if key == ii["Answer"]:
                found_key = True
                new_guesses += jj+", "
        if not found_key:
            top_mismatch += 1
            print "TOP GUESS NOT OF PRONOUN TYPE", top_mismatch
        #reset CSV iterator
        answer_info_file.seek(0)
    #print "MOST COMMON PRONOUN : ", pronouns
    #print "CLEANED GUESSES :", new_guesses
    #print "OLD GUESSES :", guesses
    #print ""
    """ remove last ', ' """
    new_guesses = new_guesses[:-2]
    print new_guesses
    return new_guesses

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
    # find pronouns
    pronouns = find_pronouns(ii['Question Text'])
    # find the most common pronoun
    pronoun = most_common_pronoun(pronouns)
    # cleaning QANTA guesses before procesing
    Q_clean_text = clean_guesses(ii['QANTA Scores'], pronoun)
    # cleaning IR_WIKI guesses before procesing
    IR_clean_text = clean_guesses(ii['QANTA Scores'], pronoun)
    Q_dict = guess_score_dict(Q_clean_text)
    for key in Q_dict.keys():
        Q_score_dict[(ii['Question ID'],key)] = Q_dict[key]
    IR_dict = guess_score_dict(IR_clean_text)
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
