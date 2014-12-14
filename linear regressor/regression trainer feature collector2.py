import nltk.classify.maxent
from nltk.classify.maxent import MaxentClassifier
# C:\Python27\lib\site-packages\nltk\classify\maxent.py
from nltk.classify.util import accuracy 
# C:\Python27\lib\site-packages\nltk\classify\util.py
from nltk.tokenize import word_tokenize

from csv import DictReader, DictWriter
from collections import defaultdict

from random import shuffle

# VARIABLES:
WRITE_FILE = 1

# number of questions to include in training set:
COLLECT_ONE_OUT_OF = 1 

# number of wrong answers for each question to include:
NUM_BAD_ANSWERS = 20

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

key_file_name = "../csv/train.csv"
key_data = DictReader(open(key_file_name, 'r'))

outfile_name = "features_train2.csv"

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
        # find pronouns
        pronouns = find_pronouns(ii['Question Text'])
        # find the most common pronoun
        pronoun = most_common_pronoun(pronouns)
        # cleaning QANTA guesses before procesing
        Q_clean_text = clean_guesses(ii['QANTA Scores'], pronoun)
        # cleaning IR_WIKI guesses before procesing
        IR_clean_text = clean_guesses(ii['QANTA Scores'], pronoun)
        # split the answer fields into seperate anwers
        Q_d = guess_score_dict(Q_clean_text)
        IR_d = guess_score_dict(IR_clean_text)

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
