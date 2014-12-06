import random
from csv import DictReader, DictWriter
from string import replace
import nltk
import re
import json
import urllib

FREEBASE_KEY = "AIzaSyB0ZlL_8WOWRnDBDka2Y5ZWmlw2xjLKvKc"
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

    
def is_person(possible_name):
    """
    Use freebase to know if answere is a person and return boolean
    """
    freebase_server = "https://www.googleapis.com/freebase/v1/search"
    params = {
            "key": FREEBASE_KEY,
            "query": possible_name,
            "filter": "(any type:/people/person)"
        }
    url = freebase_server + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    try:
        for result in response['result']:
            if re.sub(r' \(\w+\)',"",possible_name) == result['name'].lower():
                #print possible_name, result['name'] + ' (' + str(result['score']) + ')'
                return True
            else:
                return False
    except KeyError:
        print "make sure your Freebase key is up to date"

def clean_guesses(guesses):
    """
    returns the guesses as a string with only relevent guesses
    """
    person_guesses = ""
    thing_guesses = ""
    for jj in guesses.split(", "):
        answer = jj.split(":")
        key_spaced = re.sub("_"," ",answer[0])
        #key_spaced = re.sub(r' \(\w+\)',"",key_spaced)
        #print key_spaced
        if is_person(key_spaced):
            person_guesses += jj+", "
        else:
            thing_guesses += jj+", "
            
    """ remove last two chars (, ) """
    person_guesses = person_guesses[:-2]
    thing_guesses = thing_guesses[:-2]
    #print "PERSON"
    #print person_guesses
    #print ""
    #print "THING"
    #print thing_guesses
    #print ""
    return (person_guesses, thing_guesses)
        

if __name__ == "__main__":
    
    print "read training data answer"
    
    # Read in training data
    train = DictReader(open("../train.csv", 'rU'))
    
    # Create File for predictions
    output = DictWriter(open('answer_ner.csv', 'w'), ['Answer','type'], lineterminator='\n')
    output.writeheader()
    
    train_examples = 0
    
    for ii in train:
        train_examples += 1
        print train_examples
        QANTA_person_guesses, QANTA_thing_guesses = clean_guesses(ii['QANTA Scores'])
        IR_Wiki_person_guesses, IR_Wiki_thing_guesses = clean_guesses(ii['IR_Wiki Scores'])
        
    #print QANTA_person_guesses, QANTA_thing_guesses
    #print IR_Wiki_person_guesses, IR_Wiki_thing_guesses
    
    for jj in QANTA_person_guesses.split(", "):
        answer = jj.split(":")
        output.writerow({'Answer': answer[0], \
                    'type': "PERSON", })
    for jj in QANTA_thing_guesses.split(", "):
        answer = jj.split(":")
        output.writerow({'Answer': answer[0], \
                    'type': "THING", })
    for jj in IR_Wiki_person_guesses.split(", "):
        answer = jj.split(":")
        output.writerow({'Answer': answer[0], \
                    'type': "PERSON", })
    for jj in IR_Wiki_thing_guesses.split(", "):
        answer = jj.split(":")
        output.writerow({'Answer': answer[0], \
                    'type': "THING", })
        
    print "wrote", train_examples , "answer types"
                       