from csv import DictReader, DictWriter

import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist

""" train fields:
Question ID,
Question Text
"""

""" test fields:
Question ID,
Question Text
"""
masc_pronouns = ['he', 'him', 'his', 'himself', 'who', 'whose', 'whom']
fem_pronouns = ['she', 'her', 'hers', 'herself', 'who', 'whose', 'whom']
neut_pronouns = ['it', 'that', 'its', 'itself', 'which', 'that']
plural_pronouns = ['they', 'them', 'their', 'theirs', 'which', 'that']


SCRUB_TRAIN = 0

if __name__ == "__main__":

    if SCRUB_TRAIN:
        print "going with training data"
        data = DictReader(open("../csv/train.csv", 'r'))
        save_name = "pronouns_train.csv"
    else:
        print "going with test data"
        data = DictReader(open("../csv/test.csv", 'r'))
        save_name = "pronouns_test.csv"

    # Create File for writing
    outfile = open(save_name, 'w')
    o = DictWriter(outfile, ['Question ID','Sentence Position','Male Pronoun', 'Female Pronoun', 'Neuter Pronoun', 'Plural Pronoun'], lineterminator='\n')
    o.writeheader()
    
    data_examples = 0

    for ii in data:
        data_examples += 1

        male = 0
        female = 0
        neuter = 0
        plural = 0

        # Split question on words:
        word_list = nltk.word_tokenize(ii['Question Text'])
        clean_words = []
        for word in word_list:
            if word[-1] == '.' and word != '.':               # scrub trailing periods from last words of sentences
                word = word[0:len(word)-1]

            if word in masc_pronouns:
                male += 1
            if word in fem_pronouns:
                female += 1
            if word in neut_pronouns:
                neuter += 1
            if word in plural_pronouns:
                plural += 1

        o.writerow({'Question ID': ii['Question ID'], \
                'Sentence Position': ii['Sentence Position'], \
                'Male Pronoun': male, \
                'Female Pronoun': female, \
                'Neuter Pronoun': neuter, \
                'Plural Pronoun': plural})

    outfile.close()
    print "wrote", data_examples, "lines"
