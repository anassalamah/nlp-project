import nltk.classify.maxent
from nltk.classify.maxent import MaxentClassifier
# C:\Python27\lib\site-packages\nltk\classify\maxent.py
from nltk.classify.util import accuracy 
# C:\Python27\lib\site-packages\nltk\classify\util.py

from csv import DictReader, DictWriter

# for names_demo:
from nltk.corpus import names
import random
from random import shuffle

# VARIABLES:
NUM_TRAIN_ITERATIONS = 3
PRINT_OUTPUT_TABLE = 1
NUM_TO_SCREEN_PRINT = 10

USE_VALIDATION = 1 # NOT IMPLEMENTED
USE_TEST_AND_WRITE_OUTPUT = 1

VALIDATION_FRACTION_ONE_OUT_OF = 5

test_filename = "featuresW_test.csv"
train_filename = "featuresW_train.csv"

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

#algorithm = nltk.classify.MaxentClassifier.ALGORITHMS[0] # UNKNOWN CODE



print "Reading training file:", train_filename
data = DictReader(open(train_filename, 'r'))

train_input = []
train_input_guesses = []
"""
'Question ID'
'Sentence Position'
'Answer'
'is correct'
'Q score'
'IR score'
'join score'
'category'
"""
num_read = 0
print "guess how many?"
for ii in data:
    num_read += 1
    #if random.random() > 0.6:
    if ii['is correct'] == '1' or random.random() > 0.7:
        correct = 'correct' if ii['is correct'] == '1' else 'wrong'
        #print ii['Question ID'], correct
        feat_dict = dict()
        feat_dict['BIAS'] = float(1)
        feat_dict['Q score'] = float(ii['Q score'])
        feat_dict['IR score'] = float(ii['IR score'])
        feat_dict['join score'] = float(ii['join score'])
        feat_dict['Sentence Position'] = float(ii['Sentence Position'])
        feat_dict['category'] = ii['category']
        feat_dict['Wikipedia Score'] = float(ii['Wikipedia Score'])
        feat_dict['Wikipedia Found'] = float(ii['Wikipedia Found'])
        #feat_dict['SearchWords'] = float(ii['SearchWords'])
        #feat_dict['SearchFound'] = float(ii['SearchFound'])
        #feat_dict['WikipediaLen'] = float(ii['WikipediaLen'])

        train_input = train_input + [(feat_dict,correct)]
        train_input_guesses = train_input_guesses + [(ii['Question ID'], ii['Sentence Position'], ii['Answer'], ii['is correct'])]
    if num_read % 10000 == 0:
        print num_read, "/ 371000"

if USE_VALIDATION:
    print "you want to validate, great. This is always on, you have no choice."
    
print "Splitting off validation set"

# Split off a validation subset:
train_subset = []
train_subset_guesses = []
validation_subset = []
validation_subset_guesses = []

input_size = len(train_input)

print "Shuffle input"
shuffle(train_input)

val_size = input_size/VALIDATION_FRACTION_ONE_OUT_OF

validation_subset = train_input[:val_size]
validation_subset_guesses = train_input_guesses[:val_size]
train_subset = train_input[val_size:]
train_subset_guesses = train_input_guesses[val_size:]

#for i in range(len(train_input)):
#    if i % VALIDATION_FRACTION_ONE_OUT_OF == 0:
#        validation_subset = validation_subset + [train_input[i]]
#        validation_subset_guesses = validation_subset_guesses + [train_input_guesses[i]]
#    else:
#        train_subset = train_subset + [train_input[i]]
#        train_subset_guesses = train_subset_guesses + [train_input_guesses[i]]

print "Training on", len(train_subset), "examples"

# TRAINING HERE:    
#classifier = trainer(train_subset, max_iter=NUM_TRAIN_ITERATIONS) # DEFAULT ALGORITHM
classifier = trainer(train_subset, algorithm='GIS', max_iter=NUM_TRAIN_ITERATIONS)
print "done training"

# Run the classifier on the validation data.
print 'Validating classifier on ', len(validation_subset), "examples"

acc = accuracy(classifier, validation_subset)
print('Accuracy: %6.4f' % acc)

# For classifiers that can find probabilities, show the log
# likelihood and some sample probability distributions.
test_featuresets = [feat_d for (feat_d,g) in validation_subset]

pdists = classifier.prob_classify_many(test_featuresets)

if PRINT_OUTPUT_TABLE:
    print_table(pdists, validation_subset_guesses, NUM_TO_SCREEN_PRINT)

    print "WEIGHTS:"
    print classifier.weights()

    print "MOST INTERESTING FEATURES:"
    print classifier.show_most_informative_features(10)

print "TRAINING (VALIDATION) accuracy:", acc
prob_percent = sum([pdist.prob('correct') for pdist in pdists])/len(pdists)
print "percent claim as correct:", prob_percent

print "RETRAIN ON ALL DATA"
#classifier = trainer(train_subset+validation_subset, max_iter=NUM_TRAIN_ITERATIONS) # DEFAULT ALGORITHM
classifier = trainer(train_subset+validation_subset, algorithm='GIS', max_iter=NUM_TRAIN_ITERATIONS)

if USE_TEST_AND_WRITE_OUTPUT:
    print "Going to use test files"
    data = DictReader(open(test_filename, 'r'))
    test_input = []
    test_guesses = []
    test_ID = []
    """
    'Question ID'
    'Sentence Position'
    'Answer'
    'Q score'
    'IR score'
    'join score'
    'category'
    """
    for ii in data:
        feat_dict = dict()
        feat_dict['BIAS'] = float(1)
        feat_dict['Q score'] = float(ii['Q score'])
        feat_dict['IR score'] = float(ii['IR score'])
        feat_dict['Sentence Position'] = float(ii['Sentence Position'])
        feat_dict['category'] = ii['category']
        feat_dict['join score'] = float(ii['join score'])
        feat_dict['Wikipedia Score'] = float(ii['Wikipedia Score'])
        feat_dict['Wikipedia Found'] = float(ii['Wikipedia Found'])
        #feat_dict['SearchWords'] = float(ii['SearchWords'])
        #feat_dict['SearchFound'] = float(ii['SearchFound'])
        #feat_dict['WikipediaLen'] = float(ii['WikipediaLen'])

        test_input = test_input + [feat_dict]
        test_guesses = test_guesses + [ii['Answer']]
        test_ID = test_ID + [ii['Question ID']]

    # compute probabilities
    print "TEST: computing probabilities"
    pdists = classifier.prob_classify_many(test_input)

    # prepare to write output file
    outfile_name = "test_guesses_POLYLINE_W.csv"
    outfile = open(outfile_name, 'w')
    o = DictWriter(outfile, ['Question ID','Answer','Prob'], lineterminator='\n')
    o.writeheader()

    for i in range(len(pdists)):
        o.writerow({'Question ID': test_ID[i], \
                    'Answer': test_guesses[i], \
                    'Prob': pdists[i].prob('correct') })

    outfile.close() 
    print "wrote", len(test_input), "lines of guess probabilities"

print "DONE"
