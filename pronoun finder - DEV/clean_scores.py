from collections import defaultdict
from csv import DictReader, DictWriter

import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import TreebankWordTokenizer
from nltk.tokenize import word_tokenize
from nltk import FreqDist
import re
import string
import random

kTOKENIZER = TreebankWordTokenizer()
person_pronouns = ['he','him','his','she','her','hers','himself','herself','each other',"each other's", 'one another', "one another's",'who','whoever','whomever','whom','whose'] 
thing_pronouns = ["it", "its"]
group_pronouns= ['they", "them", "their", theirs']
all_pronouns = person_pronouns + thing_pronouns + group_pronouns

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



def find_pronouns(text):
    tokens = word_tokenize(text)
    print tokens
    pronouns  = []
    for i in tokens:
        if i in all_pronouns:
            pronouns.append(i)
    print pronouns
    return pronouns

def most_common_pronoun(pronouns):
    """
    return the most common pronoun,
    and in the case of many having the same count return the first one
    """
    if pronouns:
        pronouns = max(set(pronouns), key= lambda x: (pronouns.count, -pronouns.index(x)))
        
    return pronouns
    
def clean_guesses(guesses, pronouns):
    if pronouns in person_pronouns:
        # Read in person INFO
        answer_info_file = open("csv/person_info.csv", 'r')
        answer_info = DictReader(answer_info_file)
    elif not pronouns:
        print "PRONOUNS EMPTY", 
        return guesses
    else:
        # Read in non_person NER
        answer_info_file = open("csv/non_person_info.csv", 'r')
        answer_info = DictReader(answer_info_file)
    new_guesses= ""
    for jj in guesses.split(", "):
        #print jj
        key,val = jj.split(":")
        for ii in answer_info:
            if key == ii["Answer"]:
                new_guesses += jj+", "
        #reset CSV iterator
        answer_info_file.seek(0)
    #print "MOST COMMON PRONOUN : ", pronouns
    #print "CLEANED GUESSES :", new_guesses
    #print "OLD GUESSES :", guesses
    #print ""
    """ remove last ', ' """
    new_guesses = new_guesses[:-2]
    return new_guesses          
        
    

debug = 0

if __name__ == "__main__":

    print "read training data"
    
    # Read input train.csv or test.csv
    inp = DictReader(open("csv/train.csv", 'r'))

    Q_train = []
    IR_train = []

    train_examples = 0
    
    for ii in inp:
        train_examples += 1
        print "TRAIN: ", train_examples
        Question_text = ii['Question Text']
        QANTA_scores = ii['QANTA Scores']
        IR_Wiki_scores = ii['IR_Wiki Scores']
        answer = ii['Answer']
        print Question_text
        #print ii['Question Text']
        pronouns = find_pronouns(Question_text)
        pronoun = most_common_pronoun(pronouns)
        print pronoun
        print "QANTA: "
        print "ORG: ", QANTA_scores
        print ""
        QANTA_clean_scores = clean_guesses(QANTA_scores, pronouns)
        print "CLEAN: ", QANTA_clean_scores
        print "IR_WIKI: "
        print "ORG: ", IR_Wiki_scores
        print ""
        IR_Wiki_clean_scores = clean_guesses(IR_Wiki_scores, pronouns)
        print "CLEAN: ", IR_Wiki_clean_scores

    
