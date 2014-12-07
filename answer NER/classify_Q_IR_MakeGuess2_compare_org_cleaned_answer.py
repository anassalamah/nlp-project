from collections import defaultdict
from csv import DictReader, DictWriter

import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import TreebankWordTokenizer

from nltk import FreqDist
import re
import string

kTOKENIZER = TreebankWordTokenizer()
person_pronouns = ["he","his","himself","someone","who","she","her","herself"]

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

def top_guess(guesses):
    """
    returns a tuple of the top guess and value of that guess
    """
    #d = defaultdict(float)
    for jj in guesses.split(", "):
        key,val = jj.split(":")
        #d[key.strip()] = float(val)
        break
    return (key, float(val))

def find_pronouns(text):
    pronouns = re.findall(" he | his | himself | someone | who", text)
    pronouns = pronouns + re.findall(" she | her | herself", text)
    pronouns = pronouns + re.findall(" they | them | those | their | themselves ", text)
    pronouns = pronouns + re.findall(" its | it | itself | something | what ", text)

    clean_pronouns = []
    for i in pronouns:
        clean_pronouns = clean_pronouns + [i.strip()]
    
    return clean_pronouns


def features(case):
    d = defaultdict()
    d["category"] = case['category']
    d["Sentence Position"] = case['Sentence Position']

    return d


def clean_guesses(guesses, pronouns):
    # Read in answer NER
    answer_file = open("../csv/answer_ner.csv", 'r')
    answer_ner = DictReader(answer_file)
    
    # give me the most common pronoun only
    if pronouns:
        pronouns = max(set(pronouns), key=pronouns.count)
        
    new_guesses= ""
    for jj in guesses.split(", "):
        #print jj
        key,val = jj.split(":")
        for ii in answer_ner:
            if key == ii["Answer"]:
                if pronouns in person_pronouns:
                    if ii["Person"] == '1':
                        new_guesses += jj+", "
                else:
                    if ii["Person"] != '1':
                        new_guesses += jj+", "
        #reset CSV iterator
        answer_file.seek(0) 
        
    """ remove last ', ' """
    new_guesses = new_guesses[:-2]
    return new_guesses          
        
    

debug = 0

if __name__ == "__main__":

    print "read training data"
    
    # Read in training data
    train = DictReader(open("../csv/train.csv", 'r'))

    Q_train = []
    IR_train = []

    train_examples = 0
    
    for ii in train:
        train_examples += 1
        if train_examples == 1:
            print "TRAIN: ", train_examples
            feat = features(ii)
            pronouns = find_pronouns(ii['Question Text']) 

            QANTA_clean_guesses = clean_guesses(ii['QANTA Scores'], pronouns)
            if QANTA_clean_guesses:
                Q_guess, Q_confidence = top_guess(QANTA_clean_guesses)
            else:
                print "CLEAN QANTA GUESSES WERE EMPTY"
                Q_guess, Q_confidence = top_guess(ii['QANTA Scores'])

            IR_Wiki_clean_guesses = clean_guesses(ii['IR_Wiki Scores'], pronouns)
            if IR_Wiki_clean_guesses:
                IR_guess, IR_confidence = top_guess(IR_Wiki_clean_guesses)
            else:
                print "CLEAN IR GUESSES WERE EMPTY"
                IR_guess, IR_confidence = top_guess(ii['IR_Wiki Scores'])

            if Q_guess == ii['Answer']:
                correct = 'right'
            else:
                correct = 'wrong'
            Q_train.append((feat, correct))

            if IR_guess == ii['Answer']:
                correct = 'right'
            else:
                correct = 'wrong'
            IR_train.append((feat, correct))


            if debug == 1:
                print "example " + str(train_examples)
                print "feat:", feat
    
    # Train a classifier
    print("Training classifier ...")
    Q_classifier = nltk.classify.NaiveBayesClassifier.train(Q_train)
    IR_classifier = nltk.classify.NaiveBayesClassifier.train(IR_train)

    print "looked at", train_examples, "examples"
    
    # Test a classifier
    print("Ready to test")

    test = DictReader(open("../csv/test.csv", 'r'))

    # Create File for predictions
    o = DictWriter(open('NBpred2.csv', 'w'), ['Question ID','Answer'])
    o.writeheader()
    
    test_examples = 0

    for ii in test:
        test_examples += 1
        print "TEST: ", test_examples
        feat = features(ii)
        pronouns = find_pronouns(ii['Question Text']) 
		
        QANTA_clean_guesses = clean_guesses(ii['QANTA Scores'], pronouns)
        if QANTA_clean_guesses:
            Q_guess, Q_confidence = top_guess(QANTA_clean_guesses)
        else:
            print "CLEAN QANTA GUESSES WERE EMPTY"
            Q_guess, Q_confidence = top_guess(ii['QANTA Scores'])

        IR_Wiki_clean_guesses = clean_guesses(ii['IR_Wiki Scores'], pronouns)
        if IR_Wiki_clean_guesses:
            IR_guess, IR_confidence = top_guess(IR_Wiki_clean_guesses)
        else:
            print "CLEAN IR GUESSES WERE EMPTY"
            IR_guess, IR_confidence = top_guess(ii['IR_Wiki Scores'])

        Q_pred = Q_classifier.classify(feat)
        Q_prob_dist = Q_classifier.prob_classify(feat)
        IR_pred = IR_classifier.classify(feat)
        IR_prob_dist = IR_classifier.prob_classify(feat)

        if Q_prob_dist.prob('right') > IR_prob_dist.prob('right'):
            best_guess = Q_guess
        else:
            best_guess = IR_guess
    
        o.writerow({'Question ID': ii['Question ID'], 'Answer': best_guess})

    print "made", test_examples, "guesses"


#            print "sentence position:", str(sp)
#            print "category:", cat
#            print "QANTA:  ", Q_pred, "(", Q_prob_dist.prob('right'), ")"
#            print "IR_Wiki:", IR_pred, "(", IR_prob_dist.prob('right'), ")"
#            print ""

