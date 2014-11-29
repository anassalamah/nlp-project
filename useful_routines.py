""" these may or may not be needed """
from collections import defaultdict
#from csv import DictReader, DictWriter
#import nltk
#from nltk.corpus import wordnet as wn
#from nltk.tokenize import TreebankWordTokenizer
#from nltk import FreqDist
#import string

def form_dict(vals):
    """
    this code given to us in the project readme
    returns a dict with guesses as the keys, and guess confidence
    as the values
    """
    d = defaultdict(float)
    for jj in vals.split(", "):
        key, val = jj.split(":")
        d[key.strip()] = float(val)
    return d

def top_guess(vals):
    """
    returns a tuple of the top guess and value of that guess
    """
    d = defaultdict(float)
    for jj in vals.split(", "):
        key, val = jj.split(":")
        #d[key.strip()] = float(val)
        break
    return (key, float(val))

def split_question_sents(text, num_expected):
    """
    takes the question text and returns it as a list of sentences
    """
    sents = []
    for s in text.split("."):
        sents.append(s.strip())

    # in most (all?) cases, there will be an empty element addded at the end (something after the . ?)
    del sents[-1]   # cleans up the empty entry

    if len(sents) != num_expected:
        print "ERROR, num sentences is unexpected"

    return sents
