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
    
def search_for_person_freebase(link):
    """
    Use freebase to know if answere is a person and return boolean
    """
    clean_link = re.sub("_"," ",link)
    
    freebase_server = "https://www.googleapis.com/freebase/v1/search"
    params = {
            "key": FREEBASE_KEY,
            "query": clean_link,
            "limit": 3,                             #limit of top 3 hits
            "filter": "(all type:/people/person)",  #only person type
            "output": '(description)'               #add their description
        }
    # Make search
    url = freebase_server + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    
    # Check for errors and exit with a message if the query failed.
    try:
        response['status']
    except KeyError:
        error = response['error']
        sys.exit('%s: %s' % (error['code'], error['message'])) # Display code,msg.
    
    # No errors, so handle the result
    results = response['result']           # Open the response envelope, get result.
    
    print "FREEBASING:", link
    description_list=[]
    type_list=[]
    for ii in results:
        description_list += ii['output']['description']['/common/topic/description']
        #if ii['notable']:
            #type_list += ii['notable']['name']
            #type_list += ii['id'].split('/')
            #print ii
            #print "ID", ii['notable']['name']
    #print type_list
    return description_list

if __name__ == "__main__":
    
    print "read training data answer"
    
    # Read in training data
    answers = DictReader(open("wiki_links.csv", 'rU'))
    
    # Create File for predictions
    output = DictWriter(open('answer_ner2.csv', 'w'), ['Answer','Person','Description', "type"], lineterminator='\n')
    output.writeheader()
    
    answer_counts = 0
    
    for ii in answers:
        answer_counts += 1
        if answer_counts < 10:
            print "Answer Number: ", answer_counts
            result = search_for_person_freebase(ii["link"])
            if result:
                for hit in result:
                    #print hit
                    #print ''
                    output.writerow({'Answer': ii["link"], \
                                     'Person': 1, \
                                    'Description': hit.encode('utf8')})
       
    
   
    print "wrote", answer_counts , "answer types"
                       