import random
from csv import DictReader, DictWriter
from string import replace
import nltk
import re
import json
import urllib
import time
FREEBASE_KEY = "AIzaSyClHgL3It7_9vtJAmekhlSp7ucMw_rwAJU"
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

    
def is_person(link):
    """
    Use freebase to know if answere is a person and return boolean
    """
    clean_link = re.sub("_"," ",link)
    freebase_server = "https://www.googleapis.com/freebase/v1/search"
    params = {
            "key": FREEBASE_KEY,
            "query": clean_link,
            "filter": "(any type:/people/person)"
        }
    url = freebase_server + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    
    
    for result in response['result']:
        if re.sub(r' \(\w+\)',"",clean_link) == result['name'].lower():
            #print clean_link, result['name'] + ' (' + str(result['score']) + ')'
            return 1
        else:
            return 0
        

if __name__ == "__main__":
    
    print "read training data answer"
    
    # Read in training data
    answers = DictReader(open("wiki_links.csv", 'rU'))
    
    # Create File for predictions
    output = DictWriter(open('answer_ner.csv', 'w'), ['Answer','Person'], lineterminator='\n')
    output.writeheader()
    
    answer_counts = 0
    
    for ii in answers:
        answer_counts += 1
        print "Answer Number: ", answer_counts
        output.writerow({'Answer': ii["link"], \
                    'Person': is_person(ii["link"]) })
       
    
   
    print "wrote", answer_counts , "answer types"
                       