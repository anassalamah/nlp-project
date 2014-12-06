from collections import defaultdict
from csv import DictReader, DictWriter

import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import TreebankWordTokenizer

from nltk import FreqDist

import string

kTOKENIZER = TreebankWordTokenizer()

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
    d = defaultdict(float)
    for jj in guesses.split(", "):
        key, val = jj.split(":")
        #d[key.strip()] = float(val)
        break
    return (key, float(val))


def features(case):
    d = defaultdict()
    d["category"] = case['category']
    d["Sentence Position"] = case['Sentence Position']

    return d


debug = 0

if __name__ == "__main__":

    print "read training data"
    
    # Read in training data
    #train = DictReader(open("../csv/train_SS3.csv", 'r'))
    train = DictReader(open("../csv/train.csv", 'r'))


    Q_train = []
    IR_train = []

    train_examples = 0
    
    for ii in train:
        train_examples += 1

        feat = features(ii)

        Q_guess, Q_confidence = top_guess(ii['QANTA Scores'])
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
    
    print("how good is this?\n")
    # Test a classifier

    print "BY SENTENCE POSITION\n"
    for sp in [0,1,2,3,4]:
        Q_pred = Q_classifier.classify({'Sentence Position': str(sp)})
        Q_prob_dist = Q_classifier.prob_classify({'Sentence Position': str(sp)})
        IR_pred = IR_classifier.classify({'Sentence Position': str(sp)})
        IR_prob_dist = IR_classifier.prob_classify({'Sentence Position': str(sp)})
        print "sentence position:", str(sp)
        print "QANTA:  ", Q_pred, "(", Q_prob_dist.prob('right'), ")"
        print "IR_Wiki:", IR_pred, "(", IR_prob_dist.prob('right'), ")"
        print ""

    print "BY CATEGORY\n"        
    for cat in ['science','lit','social','history']:
        Q_pred = Q_classifier.classify({'category': cat})
        Q_prob_dist = Q_classifier.prob_classify({'category': cat})
        IR_pred = IR_classifier.classify({'category': cat})
        IR_prob_dist = IR_classifier.prob_classify({'category': cat})
        print "category:", cat
        print "QANTA:  ", Q_pred, "(", Q_prob_dist.prob('right'), ")"
        print "IR_Wiki:", IR_pred, "(", IR_prob_dist.prob('right'), ")"
        print ""
    
