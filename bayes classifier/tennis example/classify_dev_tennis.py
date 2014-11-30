from collections import defaultdict
from csv import DictReader, DictWriter

import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import TreebankWordTokenizer

from nltk import FreqDist

import string

kTOKENIZER = TreebankWordTokenizer()




def features(case):
    d = defaultdict()
    d["outlook"] = case['outlook']
    d["temperature"] = case['temperature']
    d["humidity"] = case['humidity']
    d["wind"] = case['wind']
    

    return d


debug = 1

if __name__ == "__main__":

    print "read training data"
    
    # Read in training data
    train = DictReader(open("tennis3.csv", 'r'))

    dev_train = []

    train_examples = 0
    all_samples = 0
    key_inp = 'a'

    for ii in train:
        all_samples += 1

        train_examples += 1

        print ii
        print "outlook:", ii['outlook']
        print "temperature:", ii['temperature']
        print "humidity:", ii['humidity']
        print "wind:", ii['wind']
        print "play:", ii['play']

        feat = features(ii)
        dev_train.append((feat, ii['play']))
        
        if debug == 1:
            print "example " + str(train_examples)
            print defaultdict(ii)
            print "feat:", feat
    
    # Train a classifier
    print("Training classifier ...")
    classifier = nltk.classify.NaiveBayesClassifier.train(dev_train)
    
    #prediction = classifier.classify(ii[0])
    prediction = classifier.classify({'outlook': 'Rain', 'temperature': 'Mild'})
    prob_dist = classifier.prob_classify({'outlook': 'Rain', 'temperature': 'Mild'})
    print "prediction:", prediction,
    #for prob in prob_dist:
    #    print prob
    print prob_dist.prob('Yes')
    print prob_dist.prob('No')
        
    prediction = classifier.classify({'outlook': 'Rain', 'temperature': 'Hot'})
    prob_dist = classifier.prob_classify({'outlook': 'Rain', 'temperature': 'Hot'})
    print "prediction:", prediction,
    #for prob in prob_dist:
    #    print prob
    print prob_dist.prob('Yes')
    print prob_dist.prob('No')
