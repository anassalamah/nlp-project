# Author: Anas Salamah
# Date: Oct 3, 2014

from collections import defaultdict
from csv import DictReader, DictWriter
import re


import nltk
from nltk.corpus import wordnet as wn, stopwords as sw
from nltk.tokenize import TreebankWordTokenizer, RegexpTokenizer
from nltk import pos_tag, word_tokenize

wTOKENIZER = RegexpTokenizer(r'\w+')


def morphy_stem(word):
    """
    Simple stemmer
    """
    stem = wn.morphy(word)
    if stem:
        return stem.lower()
    else:
        return word.lower()

class FeatureExtractor:
    def __init__(self):
        None
    			
    def features(self, text):
        d = defaultdict(int)
        for ii in pos_tag(word_tokenize(text)):
            if ii[1] == "PRP" or ii[1] == "PRP$":
                d[ii[0]] += 1
            #for cc in sw.words():
        	#if morphy_stem(ii) == cc:
        	    #d["StopW"] += 1
	    """if ii[-2:] == 'ed':
            	d["PV"] += 1
            elif ii[-3:] == 'ing':
            	d["PresV"] += 1
            elif ii[-2:] == 'ly':
            	d["ADV"] += 1
            
            if ii[0].isupper():
            	d["PV"] += 1"""
        	
        #d["DOCLEN"] = len(list(wTOKENIZER.tokenize(text)))
        return d

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--subsample', type=float, default=1.0,
                        help='subsample this amount')
    args = parser.parse_args()
    
    # Create feature extractor (you may want to modify this)
    fe = FeatureExtractor()
    
    # Read in training data
    train = DictReader(open("train.csv", 'r'))
    
    # Split off dev section
    dev_train = []
    dev_test = []
    full_train = []

    for ii in train:
        if args.subsample < 1.0 and int(ii['Question ID']) % 100 > 100 * args.subsample:
            continue
        feat = fe.features(ii['Question Text'])
        if int(ii['Question ID']) % 5 == 0:
            dev_test.append((feat, ii['IR_Wiki Scores']))
        else:
            dev_train.append((feat, ii['IR_Wiki Scores']))
        full_train.append((feat, ii['IR_Wiki Scores']))
	
    print dev_train[0]
    # Train a classifier
    print("Training classifier ...")
    classifier = nltk.classify.NaiveBayesClassifier.train(dev_train)
    #print "self._label_probdist: ", classifier._label_probdist
    #print "" 
    #print "self._feature_probdist",classifier._feature_probdist
    #print ""
    #print  "self._labels", classifier._labels
    # classifier = nltk.classify.MaxentClassifier.train(dev_train, 'IIS', trace=3, max_iter=1000)

    right = 0
    total = len(dev_test)
    for ii in dev_test:
        prediction = classifier.classify(ii[0])
        if prediction == ii[1]:
            right += 1
    print("Accuracy on dev: %f" % (float(right) / float(total)))

    # Retrain on all data
    classifier = nltk.classify.NaiveBayesClassifier.train(dev_train + dev_test)
    
    # Read in test section
    test = {}
    for ii in DictReader(open("test.csv")):
        test[ii['Question ID']] = classifier.classify(fe.features(ii['Question ID']))

    # Write predictions
    o = DictWriter(open('pred.csv', 'w'), ['Question ID', 'pred'])
    o.writeheader()
    for ii in sorted(test):
        o.writerow({'Question ID': ii, 'pred': test[ii]})
