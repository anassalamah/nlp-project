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
            "limit": 1,                             #limit of top 3 hits
            "filter": "(not type:/people/person)",  #only person type
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
    specific_type_list=[]
    general_type_list=[]
    for ii in results:
        if re.sub(r' \(\w+\)',"",clean_link) == ii['name'].lower():
            if ii['output']['description']:
                description_list += ii['output']['description']['/common/topic/description']
            else:
                description_list += ""
            try:
                notable = ii['notable']
            except KeyError:
                return (description_list, specific_type_list, general_type_list)
            specific_type_list.append( ii['notable']['name'])
            general_type_list.append( re.sub('^,','',re.sub('_' , ' ', re.sub('/',',',ii['notable']['id'])) ))
    
    return (description_list, specific_type_list, general_type_list)

if __name__ == "__main__":
    
    print "read training data answer"
    
    # Read in training data
    answers = DictReader(open("../csv/wiki_links.csv", 'rU'))
    
    # Create File for predictions
    output = DictWriter(open('non_person_info2.csv', 'w'), ['Answer','Description'], lineterminator='\n')
    output.writeheader()
    
    answer_counts = 0
    
    for ii in answers:
        answer_counts += 1
        print "ANSWER NUMBER >>>", answer_counts
        desc, specific_type, general_type  = search_for_person_freebase(ii["link"])
    
       
        if desc:
            for hit in desc:
                    if specific_type:
                        for ee in xrange(len(specific_type)):
                            output.writerow({'Answer': ii["link"], \
                                                'Description': hit.encode('utf8')})
                    else:
                                               output.writerow({'Answer': ii["link"], \
                                                'Description': hit.encode('utf8') })
                                            
    
   
    print "wrote", answer_counts , "answer types"
                       
