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
    #train = DictReader(open("../train_SS3.csv", 'r'))
    train = DictReader(open("../train.csv", 'r'))


    dev_train = []

    train_examples = 0
    
    for ii in train:
        train_examples += 1

        feat = features(ii)

        guess, confidence = top_guess(ii['QANTA Scores'])
        
        if guess == ii['Answer']:
            correct = 'right'
        else:
            correct = 'wrong'
        dev_train.append((feat, correct))
        
        if debug == 1:
            print "example " + str(train_examples)
            print "feat:", feat
    
    # Train a classifier
    print("Training classifier ...")
    classifier = nltk.classify.NaiveBayesClassifier.train(dev_train)
    

    print("how good is this?")

    for sp in [0,1,2,3,4]:
        prediction = classifier.classify({'Sentence Position': str(sp)})
        prob_dist = classifier.prob_classify({'Sentence Position': str(sp)})
        print "sentence position:", str(sp)
        print "QANTA:", prediction
        print "right", prob_dist.prob('right')
        print "wrong", prob_dist.prob('wrong')
        print ""
            
    for cat in ['science','lit','social','history']:
        prediction = classifier.classify({'category': cat})
        prob_dist = classifier.prob_classify({'category': cat})
        print "category:", cat
        print "QANTA:", prediction
        print "right", prob_dist.prob('right')
        print "wrong", prob_dist.prob('wrong')
        print ""
    
