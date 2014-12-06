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

def find_topic_text(text, file_topics, topic_index, last_topic_index):
    """
    return the entire text of the topic
    topic_index is the list index in file_topics of the topic
    """

    # get the index in the text where the topic starts
    start = text.index(file_topics[topic_index])

    if topic_index < last_topic_index:
        # get the index in the text where the topic ends (last whitespace before next topic)
        end = text.index(file_topics[topic_index + 1]) - 1
    else:
        end = len(text) - 2


    #print start
    #print end
    return text[start:end]


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
        num_topics = len(file_topics)
        last_topic_index = num_topics - 1

        for topic in file_topics:
            topic_no_bracket_in_LOWER = topic[2:len(topic)-2].lower()
            if topic_no_bracket_in_LOWER in wiki_links_to_find_LOWER:
                wiki_links_to_find_LOWER.remove(topic_no_bracket_in_LOWER)
                found_article = topic[2:len(topic)-2]

                title = "[["+found_article+"]]"
                if title in file_topics:
                    title_index = file_topics.index(title)

                    #print title_index, "of", num_topics

                    found_text = find_topic_text(contents, file_topics, title_index, last_topic_index)
                    new_title_found_article = found_article.replace("?","")
                    new_title_found_article = new_title_found_article.replace("/","-")
                    if new_title_found_article != found_article:
                        print found_article, "->", new_title_found_article
                    writefile = open(new_title_found_article+".txt", "w")
                    writefile.write(found_text)
                    writefile.close()
                else:
                    print "whoops, thought it was in there:", title

                
                
    #break


print "DONE"
