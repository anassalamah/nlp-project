#from collections import defaultdict
from csv import DictReader, DictWriter

import nltk
from nltk.corpus import stopwords
#from nltk.corpus import wordnet as wn
#from nltk.tokenize import TreebankWordTokenizer

#from nltk import FreqDist
#import string

#kTOKENIZER = TreebankWordTokenizer()


#from useful_routines import form_dict
#from useful_routines import top_guess
#from useful_routines import split_question_sents
#from useful_routines import answer_position_in_guesses

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



if __name__ == "__main__":

    print "read training data"
    
    # Read in training data
    train = DictReader(open("../csv/train_SS3.csv", 'r'))  # SS = 'super short' training file, for debugging

    train_examples = 0

    key_inp = 'a' # dummmy value, not used

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

    for ii in train:
        train_examples += 1

        print "example", train_examples
        print "ID: " + ii['Question ID']
        print "pos: " + ii['Sentence Position']
        print "text: " + ii['Question Text']
        print "cat: " + ii['category']
        print "ans: " + ii['Answer']
        print "IR_Wiki: " + ii['IR_Wiki Scores']
        print "QANTA: " + ii['QANTA Scores']
        print ""

        sents = split_question_sents(ii['Question Text'], int(ii['Sentence Position'])+1)
        joined_sents = ' '.join(sents)
        list_sents = nltk.sent_tokenize(joined_sents)
        print list_sents
        list_sents = nltk.sent_tokenize(ii['Question Text'])
        print list_sents

        for s in list_sents:
            split_sents = nltk.word_tokenize(s)
            filtered_sents = [w for w in split_sents if not w in stopwords.words('english')]
            print filtered_sents
        
        key_inp = raw_input()

    print "DONE"
