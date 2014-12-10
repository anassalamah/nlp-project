""" these may or may not be needed """
from collections import defaultdict
#from csv import DictReader, DictWriter
#import nltk
#from nltk.corpus import wordnet as wn
#from nltk.tokenize import TreebankWordTokenizer
#from nltk import FreqDist
#import string

def form_dict(guesses):
    """
    this code given to us in the project readme
    returns a dict with guesses as the keys, and guess confidence
    as the values
    """
    d = defaultdict(float)
    for jj in guesses.split(", "):
        key, val = jj.split(":")
        d[key.strip()] = float(val)
    return d

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

def answer_position_in_guesses(guesses, answer):
    """
    returns an integer representing the position of the correct answer in the list of guesses from the computer
    note: in this function, the position is NOT an index
    index values go from 0 to n-1,
    position values go from 1 to n
    0 (zero) is returned if the answer was not found in the guesses
    comment: this is useful for the training set, usefulness in test code is yet to be determined
    """
    pos = 0
    found = 0
    for jj in guesses.split(", "):
        pos += 1
        key, val = jj.split(":")
        if key == answer:
            found = 1
            break

    if found == 0:
        pos = 0
    
    return pos


def split_question_sents(text, num_expected):
    """
    takes the question text and returns it as a list of clean sentences
    a sentence is a list of lowercase chars and symbols that has no whitespace at the beginning and end
    there is no period at the end of the sentence
    """
    sents = []
    for s in text.split("."):
        sents.append(s.strip())

    # in most (all?) cases, there will be an empty element addded at the end (something after the . ?)
    del sents[-1]   # cleans up the empty entry

    if len(sents) != num_expected:
        print "ERROR, num sentences is unexpected"
        print sents
        print num_expected
        raw_input()

    return sents
    type(sents)
