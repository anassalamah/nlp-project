#from collections import defaultdict
from csv import DictReader, DictWriter

import nltk
from nltk.corpus import stopwords
#from nltk.corpus import wordnet as wn
#from nltk.tokenize import TreebankWordTokenizer

#from nltk import FreqDist
#import string

#kTOKENIZER = TreebankWordTokenizer()


from useful_routines import form_dict
from useful_routines import top_guess
from useful_routines import split_question_sents
from useful_routines import answer_position_in_guesses

if __name__ == "__main__":

    print "read training data"
    
    # Read in training data
    train = DictReader(open("csc/train_SS3.csv", 'r'))  # SS = 'super short' training file, for debugging

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
        for s in list_sents:
            split_sents = nltk.word_tokenize(s)
            filtered_sents = [w for w in split_sents if not w in stopwords.words('english')]
            print filtered_sents
        
        
        QANTA_dict = form_dict(ii['QANTA Scores'])
        IR_dict = form_dict(ii['IR_Wiki Scores'])

        Q_num_guesses = len(QANTA_dict)
        IR_num_guesses = len(IR_dict)

        #print QANTA_dict.keys()

        #ik = QANTA_dict.iteritems()
        #for key in ik:
        #    print key

        Q_top, Q_top_score = top_guess(ii['QANTA Scores'])
        IR_top, IR_top_score = top_guess(ii['IR_Wiki Scores'])

        #print Q_top
        #print Q_top_score
        
        if ii['Answer'] in QANTA_dict:
            print "QANTA score", QANTA_dict[ii['Answer']]/Q_top_score,
            print "|", answer_position_in_guesses(ii['QANTA Scores'], ii['Answer']),
            print "/", Q_num_guesses
        else:
            print "Answer not found in QANTA"

        if ii['Answer'] in IR_dict:
            print "IR_Wiki score", IR_dict[ii['Answer']]/IR_top_score,
            print "|", answer_position_in_guesses(ii['IR_Wiki Scores'], ii['Answer']),
            print "/", IR_num_guesses
        else:
            print "Answer not found in IR_Wiki"

        key_inp = raw_input()

    print "DONE"
