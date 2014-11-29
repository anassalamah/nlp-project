#from collections import defaultdict
from csv import DictReader, DictWriter

#import nltk
#from nltk.corpus import wordnet as wn
#from nltk.tokenize import TreebankWordTokenizer

#from nltk import FreqDist
#import string

#kTOKENIZER = TreebankWordTokenizer()


from useful_routines import form_dict
from useful_routines import top_guess
from useful_routines import split_question_sents


if __name__ == "__main__":

    print "read training data"
    
    # Read in training data
    train = DictReader(open("train_SS3.csv", 'r'))  # SS = 'super short' training file, for debugging

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
        print sents
        
        QANTA_dict = form_dict(ii['QANTA Scores'])
        IR_dict = form_dict(ii['IR_Wiki Scores'])

        #print QANTA_dict.keys()

        #ik = QANTA_dict.iteritems()
        #for key in ik:
        #    print key

        Q_top, Q_top_score = top_guess(ii['QANTA Scores'])
        IR_top, IR_top_score = top_guess(ii['IR_Wiki Scores'])

        #print Q_top
        #print Q_top_score
        
        if ii['Answer'] in QANTA_dict:
            print "QANTA score", QANTA_dict[ii['Answer']]/Q_top_score
        else:
            print "Answer not found in QANTA"

        if ii['Answer'] in IR_dict:
            print "IR_Wiki score", IR_dict[ii['Answer']]/IR_top_score
        else:
            print "Answer not found in IR_Wiki"

        key_inp = raw_input()


    print "DONE"
