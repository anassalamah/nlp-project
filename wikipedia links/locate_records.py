import os
import re
from csv import DictReader, DictWriter


def strip_filenum(text):
    filenum = re.findall("00[0-9]+", text)
    return filenum[0]

def get_topics_list_bracketed(text):
    search_string = "\[\[.+\]\]"
    results = re.findall(search_string, text)

    good_results = []
    for result in results:
        if len(result) < 90:    # our longest know wiki link is 82 chars, 86 with [[]]
            good_results += [result]
    return good_results

outfile = DictWriter(open('corrected_found_links.csv', 'w'), ['search','found','file num'], lineterminator='\n')
outfile.writeheader()

wiki_links = DictReader(open("wiki_links.csv", 'r'))

wiki_links_to_find_LOWER = []
#found_list = []

for wl in wiki_links:
    link_text = wl["link"].replace("_"," ")
    wiki_links_to_find_LOWER += [link_text]
    #search_text = wl["fixed"].replace("_"," ")
    #bracketed_links_list += ["[["+search_text+"]]"] 
    #found_list += [-1]

for filename in os.listdir("../"):
    if filename.endswith(".txt"):
        readfile = open("../"+filename, 'r')   # for reading only        
        file_num = int(strip_filenum(filename))
        
        contents = readfile.read()
        file_topics = get_topics_list_bracketed(contents)

        for topic in file_topics:
            topic_no_bracket_in_LOWER = topic[2:len(topic)-2].lower()
            if topic_no_bracket_in_LOWER in wiki_links_to_find_LOWER:
                wiki_links_to_find_LOWER.remove(topic_no_bracket_in_LOWER)
                outfile.writerow({'search': topic_no_bracket_in_LOWER.replace(" ","_"), \
                                  'found': topic[2:len(topic)-2], 'file num': file_num})
                print "found:", topic[2:len(topic)-2]

    #break


for link in wiki_links_to_find_LOWER:
    outfile.writerow({'search': link.replace(" ","_"), \
                      'found': "", 'file num': -1})




print "DONE"
