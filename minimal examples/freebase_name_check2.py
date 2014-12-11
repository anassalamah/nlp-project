import sys
from collections import defaultdict
from csv import DictReader, DictWriter
from string import replace
import nltk
import json
import urllib
FREEBASE_KEY = "AIzaSyBRMODj1mCWq6CGzuGnH1BcUw_8Baqp4bw"

#import re

def search_for_person_freebase(link):
    """
    Use freebase to search for person and give me his info and a description about him
    """
    freebase_server = "https://www.googleapis.com/freebase/v1/search"
    params = {
            "key": FREEBASE_KEY,
            "query": link,
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
    
    results = response['result']
    
    print "FREEBASING:", link
    for ii in results:
        # Check the number of matching bands
        if len(ii['name']) != 0:
            print ii
            print "---------------"
    
if __name__ == "__main__":

    word_list = ["erlking", "portugal","peter the great","paraguay","samuel gompers","ethiopia","amerigo vespucci", \
             #"douglas macarthur","suez crisis","oda nobunaga","jamaica","finland","henry the navigator", \
             #"christopher columbus","emiliano zapata","vitus bering","samuel de champlain", \
             "charles de gaulle","gamal abdel nasser","haile selassie","mali empire","meiosis"]

    for word in word_list:
        search_for_person_freebase(word)

    print "DONE"
