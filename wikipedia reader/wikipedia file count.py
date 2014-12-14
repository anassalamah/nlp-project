
from csv import DictReader, DictWriter
from collections import defaultdict

import re

# VARIABLES:
WRITE_FILE = 0
TEST = 0

allcount = 0

def guess_score_dict(guesses):
    """
    returns a dictionary of ([guess] = value) of all guess
    """
    d = defaultdict(float)
    for jj in guesses.split(", "):
        key, val = jj.split(":")
        d[key.strip()] = float(val)
    
    return d

## BEGIN ##

# LOAD WIKIPEDIA TABLE
print "loading wikipeida"
wikipedialookup_file_name = "../wikipedia pages/wikipedia filename lookup.csv"
wikipedialookup = DictReader(open(wikipedialookup_file_name, 'r'))

wiki_dict = defaultdict(str)
wiki_found = defaultdict(int)
for page in wikipedialookup:
    wiki_dict[page['search']] = str(page['filename'])+".txt"
    wiki_found[page['search']] = 1 if page['found'] == 'YES' else 0

# LOAD STOPWORD TABLE
print "loading nonstop"
if TEST:
    nostopword_file_name = "../stopword remover/test_nostopwords.csv"
else:
    nostopword_file_name = "../stopword remover/train_nostopwords.csv"
nostopword = DictReader(open(nostopword_file_name, 'r'))

nostop_dict = defaultdict(str)
for ii in nostopword:
    nostop_dict[(ii['Question ID'],ii['Sentence Position'])] = str(ii['Words'])

# JOINED DATA FILE
print "loading joined data"
if TEST:
    joined_data_file_name = "../answer combiner/test Combined Scores.csv"
else:
    joined_data_file_name = "../answer combiner/train Combined Scores.csv"
joined_data = DictReader(open(joined_data_file_name, 'r'))


if WRITE_FILE:

    if TEST:
        outfile_name = "wiki_longfeatures_test.csv"
    else:
        outfile_name = "wiki_longfeatures_train.csv"
        
    # Create File for combined scores
    outfile = open(outfile_name, 'w')
    o = DictWriter(outfile, ['Question ID','Sentence Position','Answer','Wikipedia Score','Wikipedia Found','SearchWords','SearchFound','WikipediaLen'], lineterminator='\n')
    o.writeheader()

wiki_path = "../wikipedia pages/"

num_writes = 0

for ii in joined_data:
    nostop_text = nostop_dict[(ii['Question ID'],ii['Sentence Position'])].split(',')
    interest_word_count = len(nostop_text)
    
    guesses = guess_score_dict(ii['Scores'])
    for key in guesses.keys():
        allcount += 1
if WRITE_FILE:
    print "wrote", num_writes, "lines"
    outfile.close()
else:
    print "DONE", allcount
