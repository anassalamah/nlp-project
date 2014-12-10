#from collections import defaultdict
from csv import DictReader, DictWriter

import nltk
from nltk.corpus import stopwords
#from nltk.corpus import wordnet as wn
#from nltk.tokenize import TreebankWordTokenizer

#kTOKENIZER = TreebankWordTokenizer()

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

SCRUB_TRAIN = 1

if __name__ == "__main__":

    if SCRUB_TRAIN:
        print "going with training data"
        #data = DictReader(open("../csv/train_SS3.csv", 'r'))
        data = DictReader(open("../csv/train.csv", 'r'))
        save_name = "train_nostopwords.csv"
    else:
        print "going with test data"
        data = DictReader(open("../csv/test.csv", 'r'))
        save_name = "test_nostopwords.csv"

    # Create File for writing
    outfile = open(save_name, 'w')
    o = DictWriter(outfile, ['Question ID','Sentence Position','Words'], lineterminator='\n')
    o.writeheader()

    
    data_examples = 0

    for ii in data:
        data_examples += 1

        #print "ID: " + ii['Question ID']
        #print "pos: " + ii['Sentence Position']
        
        # Split question on sentences:
        # (this is just to test out nltk tokenizer)
        # maybe also try out Treebank Tokenizer? [kTOKENIZER]
        #sent_list = nltk.sent_tokenize(ii['Question Text'])
        #for sent in sent_list:
        #    print sent
        #    
        #if len(sent_list) != int(ii['Sentence Position'])+1:
        #    print "Found", len(sent_tokens), "sentences"
        #    print "Expected", int(ii['Sentence Position'])+1
        #    raw_input()

        # Split question on words:
        word_list = nltk.word_tokenize(ii['Question Text'])
        clean_words = []
        for word in word_list:
            if word != "." and word != "'s":            # throw out periods and lone-posessives
                found_word = word.replace("_"," ")
                if found_word[-1] == '.':               # scrub trailing periods from last words of sentences
                    found_word = found_word[0:len(found_word)-1]
                clean_words = clean_words + [found_word]
        filtered_words = [w for w in clean_words if not w in stopwords.words('english')]
        #print filtered_words
        #raw_input()

        word_string = ",".join(filtered_words)
        #print word_string

        o.writerow({'Question ID': ii['Question ID'], \
                    'Sentence Position': ii['Sentence Position'], \
                    'Words': word_string})
        print data_examples

    outfile.close()
    print "DONE with", data_examples



