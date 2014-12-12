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
NUM_TRAIN_ITERATIONS = 10
PRINT_OUTPUT_TABLE = 1
NUM_TO_SCREEN_PRINT = 30

USE_TRAIN = 1
USE_TEST_WRITE_OUT = 1


def feature_finder(name):
    features = {}
    #features['alwayson'] = True
    features['startswith'] = name[0].lower()
    features['endswith'] = name[-1].lower()
    #for letter in 'abcdefghijklmnopqrstuvwxyz':
    #    features['count(%s)' % letter] = name.lower().count(letter)
    #    features['has(%s)' % letter] = letter in name.lower()
    return features

def print_table(pdists, test_list, print_num = 'all'):
    ll = [pdist.logprob(gold) for ((name, gold), pdist) in zip(test_list, pdists)]
    print('Avg. log likelihood: %6.4f' % (sum(ll)/len(test_list)))
    print()
    print('Unseen Names      P(Male)  P(Female)\n'+'-'*40)

    if print_num == 'all':
        for ((name, gender), pdist) in list(zip(test_list, pdists)):
            if gender == 'male':
                fmt = '  %-15s *%6.4f   %6.4f'
            else:
                fmt = '  %-15s  %6.4f  *%6.4f'
            print(fmt % (name, pdist.prob('male'), pdist.prob('female')))
    else:
        for ((name, gender), pdist) in list(zip(test_list, pdists))[:print_num]:
            if gender == 'male':
                fmt = '  %-15s *%6.4f   %6.4f'
            else:
                fmt = '  %-15s  %6.4f  *%6.4f'
            print(fmt % (name, pdist.prob('male'), pdist.prob('female')))

## BEGIN ##

trainer = MaxentClassifier.train    # <type 'instancemethod'>

if USE_TRAIN:
    data = DictReader(open("name_features_DEV_train.csv", 'r'))
    #train_input = [(features(name), gender) for (name,gender) in train_list] # this is list of elements of <type 'tuple'>
    train_input = []
    """
    'Number'
    'Name'
    'Gender'
    'startswith'
    'endswith'
    """
    for ii in data:
        gender = ii['Gender']
        feat_dict = dict()
        feat_dict['startswith'] = ii['startswith']
        feat_dict['endswith'] = ii['endswith']
        train_input = train_input + [(feat_dict,gender)]

    # TRAINING HERE:    
    classifier = trainer(train_input , max_iter = NUM_TRAIN_ITERATIONS)

print "done train, WHAT"

# Run the classifier on the test data.
print('Testing classifier...')

test_subset = train_input[0:len(train_input):10] # 10 percent of data

acc = accuracy(classifier, test_subset)
print('Accuracy: %6.4f' % acc)

# For classifiers that can find probabilities, show the log
# likelihood and some sample probability distributions.
test_featuresets = [feat_d for (feat_d,g) in test_subset]

pdists = classifier.prob_classify_many(test_featuresets)

if PRINT_OUTPUT_TABLE:
    print_table(pdists, test_subset, NUM_TO_SCREEN_PRINT)

print "TRAINING accuracy:", acc
test_acc = sum([pdist.prob('female') for pdist in pdists])/len(pdists)
print "0 is female:", pdists[0].prob('female')
print "percent female:", test_acc

if USE_TEST_WRITE_OUT:
    data = DictReader(open("name_features_DEV_test.csv", 'r'))
    #train_input = [(features(name), gender) for (name,gender) in train_list] # this is list of elements of <type 'tuple'>
    test_input = []
    test_names = []
    test_numbers = []
    """
    'Number'
    'Name'
    'Gender'
    'startswith'
    'endswith'
    """
    for ii in data:
        #gender = ii['Gender']
        feat_dict = dict()
        feat_dict['startswith'] = ii['startswith']
        feat_dict['endswith'] = ii['endswith']
        test_input = test_input + [feat_dict]
        test_names = test_names + [ii['Name']]
        test_numbers = test_numbers + [ii['Number']]

    pdists = classifier.prob_classify_many(test_input)

    #if PRINT_OUTPUT_TABLE:
    #    print_table(pdists, test_subset, NUM_TO_SCREEN_PRINT)

    outfile_name = "test_guesses.csv"
    outfile = open(outfile_name, 'w')
    #o = DictWriter(outfile, ['Question ID','Scores'], lineterminator='\n')
    o = DictWriter(outfile, ['Number','Name','Prob'], lineterminator='\n')
    o.writeheader()

    for i in range(len(pdists)):
        #print test_numbers[i], test_names[i], pdists[i].prob('female')
        o.writerow({'Number': test_numbers[i], \
                    'Name': test_names[i], \
                    'Prob': pdists[i].prob('female') })

#    test_acc = sum([pdist.prob('female') for pdist in pdists])/len(pdists)
#    print "percent female:", test_acc

    outfile.close() 

print "DONE"
