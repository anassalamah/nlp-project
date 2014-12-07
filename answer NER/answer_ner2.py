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

    
def search_freebase(link):
    """
    Use freebase to know if answere is a person and return boolean
    """
    clean_link = re.sub("_"," ",link)
    print clean_link
    freebase_server = "https://www.googleapis.com/freebase/v1/mqlread"
    query = [{'name': clean_link, 'type': "/common/topic"}]
    params = {
            "query": json.dumps(query),
            "key": FREEBASE_KEY
        }
    url = freebase_server + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    
    print response['result']
    return response['result']
        

def top_10_freebase_pages(result):
    """
    return the top ten hits I git from get_person_info(link)
    """
    return result

if __name__ == "__main__":
    
    print "read training data answer"
    
    # Read in training data
    answers = DictReader(open("../csv/answer_ner.csv", 'rU'))
    
    # Create File for predictions
    output = DictWriter(open('answer_ner2.csv', 'w'), ['Answer','Person'], lineterminator='\n')
    output.writeheader()
    
    answer_counts = 0
    
    for ii in answers:
        answer_counts += 1
        if answer_counts < 4:
            print "Answer Number: ", answer_counts
            freebase_result = search_freebase(ii["Answer"])
            top_freebase = top_10_freebase_pages(freebase_result)
            print ii["Answer"]
            for page in top_freebase:
                print page
                print ''

            #output.writerow({'Answer': ii["Answer"], \
                    #'Person': is_person(ii["link"]) })
       
    
   
    print "wrote", answer_counts , "answer types"
                       
