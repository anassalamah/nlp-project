import nltk.classify.maxent
from nltk.classify.maxent import MaxentClassifier
# C:\Python27\lib\site-packages\nltk\classify\maxent.py
from nltk.classify.util import accuracy 
# C:\Python27\lib\site-packages\nltk\classify\util.py

from csv import DictReader, DictWriter


# for names_demo:
from nltk.corpus import names
import random

# VARIABLES:
WRITE_FILE = 1
USE_TRAIN_DATA = 0

def feature_finder(name):
    features = {}
    #features['alwayson'] = True
    features['startswith'] = name[0].lower()
    features['endswith'] = name[-1].lower()
    #for letter in 'abcdefghijklmnopqrstuvwxyz':
    #    features['count(%s)' % letter] = name.lower().count(letter)
    #    features['has(%s)' % letter] = letter in name.lower()
    return features

## BEGIN ##

if USE_TRAIN_DATA:
    outfile_name = "name_features_DEV_train.csv"
else:
    outfile_name = "name_features_DEV_test.csv"

if WRITE_FILE:
    # Create File for combined scores
    outfile = open(outfile_name, 'w')
    #o = DictWriter(outfile, ['Question ID','Scores'], lineterminator='\n')
    o = DictWriter(outfile, ['Number','Name','Gender','startswith','endswith'], lineterminator='\n')
    o.writeheader()

# Construct a list of classified names, using the names corpus.
namelist = ([(name, 'male') for name in names.words('male.txt')] +
            [(name, 'female') for name in names.words('female.txt')])

# Randomly split the names into a test & train set.
random.seed(123456)
random.shuffle(namelist)
train_list = namelist[:5000]
test_list = namelist[5000:5500]


if USE_TRAIN_DATA:
    #train_input = [(feature_finder(name), gender) for (name,gender) in train_list] # this is list of elements of <type 'tuple'>
    input_save = [(feature_finder(name), gender, name) for (name,gender) in train_list] # this is list of elements of <type 'tuple'>
else:
    #test_input = [(feature_finder(n),g) for (n,g) in test_list]
    input_save = [(feature_finder(n),g,n) for (n,g) in test_list]


outnum = 0
for ii in input_save:
    outnum += 1
    #print outnum, ii[1]
    
    feats = ii[0]
    name = ii[2]
    gender = ii[1]

    if WRITE_FILE:
        o.writerow({'Number': outnum, \
                    'Name': name, \
                    'Gender': gender, \
                    'startswith': feats['startswith'], \
                    'endswith': feats['endswith'] })

    #for key in ii[0].keys():
    #    print key, ii[0][key]

if WRITE_FILE:
    print "wrote", outnum-1, "lines"
    outfile.close()    
