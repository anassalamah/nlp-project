from collections import defaultdict
from csv import DictReader, DictWriter
from string import replace
import nltk
import json
import urllib
FREEBASE_KEY = "AIzaSyBRMODj1mCWq6CGzuGnH1BcUw_8Baqp4bw"

#import re

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

    #print "freebasing:", possible_name, response
    print "freebasing:", possible_name,

    for result in response['result']:
        if possible_name == result['name'].lower():
            print result['name'] + ' (' + str(result['score']) + ')'
            return True
        else:
            print "not found"
            return False

if __name__ == "__main__":

    word_list = ["portugal","peter the great","paraguay","samuel gompers","ethiopia","amerigo vespucci", \
             "douglas macarthur","suez crisis","oda nobunaga","jamaica","finland","henry the navigator", \
             "christopher columbus","emiliano zapata","vitus bering","samuel de champlain", \
             "charles de gaulle","gamal abdel nasser","haile selassie","mali empire"]

    for word in word_list:
        is_person(word)

    print "DONE"
