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
NUM_TRAIN_ITERATIONS = 2
PRINT_OUTPUT_TABLE = 1
NUM_TO_SCREEN_PRINT = 30

USE_TRAIN = 1
USE_TEST_WRITE_OUT = 0

def print_table(pdists, tagged_guess_list, print_num = 'all'):
    #ll = [pdist.logprob(gold) for ((name, gold), pdist) in zip(test_list, pdists)]
    #print('Avg. log likelihood: %6.4f' % (sum(ll)/len(test_list)))
    print ""
    print "Answers      P(correct)"
    print "----------------------------------------"

    if print_num == 'all':
        print_num = len(pdists)

    """ tagged_guess_list format:
    [0]: 'Question ID'
    [1]: 'Sentence Position'
    [2]: 'Answer'
    [3]: 'is correct'
    """

    for i in range(print_num):
        print tagged_guess_list[i][0]+"-"+tagged_guess_list[i][1]+"  \t",
        guess_to_print = tagged_guess_list[i][2][:20]
        guess_to_print += " "*(20-len(guess_to_print))
        print guess_to_print, 
        print "\t", tagged_guess_list[i][3], pdists[i].prob('correct')

        
## BEGIN ##

trainer = MaxentClassifier.train    # <type 'instancemethod'>

if USE_TRAIN:
    data = DictReader(open("features_DEV_train.csv", 'r'))
    #train_input = [(features(name), gender) for (name,gender) in train_list] # this is list of elements of <type 'tuple'>
    train_input = []
    train_input_guesses = []
    """
    'Question ID'
    'Sentence Position'
    'Answer'
    'is correct'
    'Q score'
    'IR score'
    """
    for ii in data:
        correct = 'correct' if ii['is correct'] == '1' else 'wrong'
        #print ii['Question ID'], correct
        feat_dict = dict()
        feat_dict['Q score'] = ii['Q score']
        feat_dict['IR score'] = ii['IR score']
        train_input = train_input + [(feat_dict,correct)]
        train_input_guesses = train_input_guesses + [(ii['Question ID'], ii['Sentence Position'], ii['Answer'], ii['is correct'])]

    # Split off a validation subset:
    train_subset = []
    train_subset_guesses = []
    validation_subset = []
    validation_subset_guesses = []
    
    for i in range(len(train_input)):
        if i % 7 == 0:
            validation_subset = validation_subset + [train_input[i]]
            validation_subset_guesses = validation_subset_guesses + [train_input_guesses[i]]
        else:
            train_subset = train_subset + [train_input[i]]
            train_subset_guesses = train_subset_guesses + [train_input_guesses[i]]

    # TRAINING HERE:    
    classifier = trainer(train_subset , max_iter = NUM_TRAIN_ITERATIONS)

print "done train, WHAT"

# Run the classifier on the test data.
print('Testing classifier...')


acc = accuracy(classifier, validation_subset)
print('Accuracy: %6.4f' % acc)

# For classifiers that can find probabilities, show the log
# likelihood and some sample probability distributions.
test_featuresets = [feat_d for (feat_d,g) in validation_subset]

pdists = classifier.prob_classify_many(test_featuresets)

if PRINT_OUTPUT_TABLE:
    #print_table(pdists, validation_subset, NUM_TO_SCREEN_PRINT)
    print_table(pdists, validation_subset_guesses, NUM_TO_SCREEN_PRINT)

print "TRAINING (VALIDATION) accuracy:", acc
prob_percent = sum([pdist.prob('correct') for pdist in pdists])/len(pdists)
#print "0 is female:", pdists[0].prob('female')
print "percent claim as correct:", prob_percent

if USE_TEST_WRITE_OUT:
    data = DictReader(open("features_DEV_test.csv", 'r'))
    #train_input = [(features(name), gender) for (name,gender) in train_list] # this is list of elements of <type 'tuple'>
    test_input = []
    test_names = []
    test_numbers = []
    """
    'Question ID'
    'Sentence Position'
    'Answer'
    'is correct'
    'Q score'
    'IR score'
    """
    for ii in data:
        feat_dict = dict()
        feat_dict['Q score'] = ii['Q score']
        feat_dict['IR score'] = ii['IR score']
        test_input = test_input + [feat_dict]
        test_guesses = test_guesses + [ii['Answer']]
        test_ID = test_ID + [ii['Question ID']]

    pdists = classifier.prob_classify_many(test_input)

    #if PRINT_OUTPUT_TABLE:
    #    print_table(pdists, test_subset, NUM_TO_SCREEN_PRINT)

    outfile_name = "test_guesses_DEV.csv"
    outfile = open(outfile_name, 'w')
    #o = DictWriter(outfile, ['Question ID','Scores'], lineterminator='\n')
    o = DictWriter(outfile, ['Question ID','Answer','Prob'], lineterminator='\n')
    o.writeheader()

    for i in range(len(pdists)):
        #print test_numbers[i], test_names[i], pdists[i].prob('female')
        o.writerow({'Question ID': test_ID[i], \
                    'Answer': test_guesses[i], \
                    'Prob': pdists[i].prob('correct') })

#    test_acc = sum([pdist.prob('female') for pdist in pdists])/len(pdists)
#    print "percent female:", test_acc

    outfile.close() 

print "DONE"
