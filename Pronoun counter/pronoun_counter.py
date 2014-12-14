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


SCRUB_TRAIN = 1

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
    o = DictWriter(outfile, ['Question ID','Sentence Position','Masculine Pronouns', 'Feminine Pronouns', 'Neuter Pronouns', 'Plural Pronouns'], lineterminator='\n')
    o.writeheader()

    
    data_examples = 0

    for ii in data:
        data_examples += 1

        # Split question on words:
        word_list = nltk.word_tokenize(ii['Question Text'])
        clean_words = []
        for word in word_list:
            if word != "." and word != "'s":            # throw out periods and lone-posessives
                found_word = word.replace("_"," ")
                if found_word[-1] == '.':               # scrub trailing periods from last words of sentences
                    found_word = found_word[0:len(found_word)-1]
                clean_words = clean_words + [found_word]
        filtered_words = [w for w in clean_words if w in stopwords.words('english')]

        #tabulating counts for different types of pronouns
        masc_pro = FreqDist([w for w in clean_words if w in masc_pronouns]).values()
        masc_pro.sort()
        masc_count = sum(masc_pro)
        
        fem_pro = FreqDist([w for w in clean_words if w in fem_pronouns]).values()
        fem_pro.sort()
        fem_count = sum(fem_pro)

        neuter_pro = FreqDist([w for w in clean_words if w in neut_pronouns]).values()
        neuter_pro.sort()
        neuter_count = sum(neuter_pro)

        plural_pro = FreqDist([w for w in clean_words if w in plural_pronouns]).values()
        plural_pro.sort()
        plural_count = sum(plural_pro)


        print 'masc:', masc_count, 'fem:', fem_count, 'neuter:', neuter_count, 'plural:', plural_count
        #raw_input()


        
        #word_string = ",".join(filtered_words)
        #fd = FreqDist(word_string)

        o.writerow({'Question ID': ii['Question ID'], \
                'Sentence Position': ii['Sentence Position'], \
                'Masculine Pronouns': masc_count, \
                'Feminine Pronouns': fem_count, \
                'Neuter Pronouns': neuter_count, \
                'Plural Pronouns': plural_count})
        

        outfile.close()
