import nltk.classify.maxent
from nltk.classify.maxent import MaxentClassifier
# C:\Python27\lib\site-packages\nltk\classify\maxent.py
from nltk.classify.util import accuracy 
# C:\Python27\lib\site-packages\nltk\classify\util.py

# for names_demo:
from nltk.corpus import names
import random

# VARIABLES:
NUM_TRAIN_ITERATIONS = 10
PRINT_OUTPUT_TABLE = 1
NUM_TO_SCREEN_PRINT = 30

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

trainer = MaxentClassifier.train    # <type 'instancemethod'>
features = feature_finder

# Construct a list of classified names, using the names corpus.
namelist = ([(name, 'male') for name in names.words('male.txt')] +
            [(name, 'female') for name in names.words('female.txt')])

# Randomly split the names into a test & train set.
random.seed(123456)
random.shuffle(namelist)
train_list = namelist[:5000]
test_list = namelist[5000:5500]

# Train a classifier.
print('Training classifier...')

train_input = [(features(name), gender) for (name,gender) in train_list] # this is list of elements of <type 'tuple'>

#train_input[0] is a tuple
#train_input[0][0] is a dict, keys are the features, vals are the feature values
#train_input[0][1] is a string representing the answer: "male" or "female"

classifier = trainer(train_input , max_iter = NUM_TRAIN_ITERATIONS)

print "WHAT"

# Run the classifier on the test data.
print('Testing classifier...')
acc = accuracy(classifier, [(features(n),g) for (n,g) in test_list])
print('Accuracy: %6.4f' % acc)

# For classifiers that can find probabilities, show the log
# likelihood and some sample probability distributions.
test_featuresets = [features(n) for (n,g) in test_list]

pdists = classifier.prob_classify_many(test_featuresets)

if PRINT_OUTPUT_TABLE:
    print_table(pdists, test_list, NUM_TO_SCREEN_PRINT)

print "TRAINING accuracy:", acc
test_acc = sum([pdist.prob('female') for pdist in pdists])/len(pdists)
print "0 is female:", pdists[0].prob('female')
print "percent female:", test_acc
