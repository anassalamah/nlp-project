from collections import defaultdict
from csv import DictReader, DictWriter
from string import replace
import nltk
import json
import urllib
#from nltk.corpus import wordnet as wn
#from nltk.tokenize import TreebankWordTokenizer
FREEBASE_KEY = "AIzaSyBRMODj1mCWq6CGzuGnH1BcUw_8Baqp4bw"
#from nltk import FreqDist

#import string

#kTOKENIZER = TreebankWordTokenizer()

import re

def find_links(text):
    links = re.findall("[a-z]+_[a-z_]+", text)
    return links

def find_this_nouns(text):
    nouns = re.findall("this ([a-z]+)", text)
    return nouns

def find_pronouns(text):
    pronouns = re.findall(" he | his ", text)
    pronouns = pronouns + re.findall(" she | her ", text)
    pronouns = pronouns + re.findall(" they | them ", text)
    pronouns = pronouns + re.findall(" its | it ", text)

    clean_pronouns = []
    for i in pronouns:
        clean_pronouns = clean_pronouns + [i.strip()]
    
    return clean_pronouns


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

def is_person(possible_name):
    """
    Use freebase to know if answere is a person and return boolean
    """
    freebase_server = "https://www.googleapis.com/freebase/v1/search"
    params = {
            "key": FREEBASE_KEY,
            "query": possible_name,
            "filter": "(any type:/people/person)"
        }

    url = freebase_server + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())

#    print "freebasing:", possible_name, response
    print "freebasing:", possible_name,


    for result in response['result']:
        if possible_name == result['name'].lower():
            print possible_name, result['name'] + ' (' + str(result['score']) + ')'
            return True
        else:
            print "not found"
            return False
    
def remove_none_types(guesses, pronouns):
    """
    returns the guesses as a string with only relevent guesses
    """
    pronouns_dict = defaultdict(int)
    """ find the count of each pronoun """
    for ii in pronouns:
        pronouns_dict[ii] += 1
    max = 0
    pronoun = ""
    """ give me the most frequent pronoun """
    for k in pronouns_dict:
        if pronouns_dict[k] > max:
            max = pronouns_dict[k]
            pronoun = k
    new_guesses= ""
    for jj in guesses.split(", "):
        key, val = jj.split(":")
        key_spaced = replace(key,"_"," ")
        if is_person(key_spaced):
            if pronoun == "he" or pronoun =="his" or pronoun =="she" or pronoun =="her":
                new_guesses += jj+", "
        else:
            new_guesses += jj+", "
    """ remove last ', ' """
    new_guesses = new_guesses[:-2]
    #print pronoun
    #print new_guesses
    return new_guesses



debug = 0

if __name__ == "__main__":

    print "read training data"
    
    # Read in training data
    train = DictReader(open("../train.csv", 'r'))

    Q_train = []
    IR_train = []

    train_examples = 0
    
    for ii in train:
        train_examples += 1

        feat = features(ii)
        pronouns = find_pronouns(ii['Question Text'])
        QANTA_new_guesses = remove_none_types(ii['QANTA Scores'], pronouns)
        WIKI_new_guesses = remove_none_types(ii['IR_Wiki Scores'], pronouns)
        Q_guess, Q_confidence = top_guess(QANTA_new_guesses)
        IR_guess, IR_confidence = top_guess(WIKI_new_guesses)
        
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

    test = DictReader(open("../test.csv", 'r'))

    # Create File for predictions
    o = DictWriter(open('printable_pred.csv', 'w'), ['ID','cat','S','Question','keywords','prob','Answer'], lineterminator='\n')
    o.writeheader()
    
    test_examples = 0

    for ii in test:
        test_examples += 1
        
        feat = features(ii)

        Q_guess, Q_confidence = top_guess(ii['QANTA Scores'])
        IR_guess, IR_confidence = top_guess(ii['IR_Wiki Scores'])

        Q_pred = Q_classifier.classify(feat)
        Q_prob_dist = Q_classifier.prob_classify(feat)
        IR_pred = IR_classifier.classify(feat)
        IR_prob_dist = IR_classifier.prob_classify(feat)

        if Q_prob_dist.prob('right') > IR_prob_dist.prob('right'):
            best_guess = Q_guess
            correct_prob = Q_prob_dist.prob('right')
        else:
            best_guess = IR_guess
            correct_prob = IR_prob_dist.prob('right')

        links = find_links(ii['Question Text'])
        nouns = find_this_nouns(ii['Question Text'])
        pronouns = find_pronouns(ii['Question Text'])

    
        o.writerow({'ID': ii['Question ID'], \
                    'cat': ii['category'], \
                    'S': ii['Sentence Position'], \
                    'Question': ii['Question Text'], \
                    'keywords': " ".join(links + nouns + pronouns), \
                    'prob': correct_prob, \
                    'Answer': best_guess})

    print "made", test_examples, "guesses" 


#            print "sentence position:", str(sp)
#            print "category:", cat
#            print "QANTA:  ", Q_pred, "(", Q_prob_dist.prob('right'), ")"
#            print "IR_Wiki:", IR_pred, "(", IR_prob_dist.prob('right'), ")"
#            print ""

