
import re

def find_links(text):
    links = re.findall("[a-z]+_[a-z_]+", text)
    return links

def find_this_nouns(text):
    nouns = re.findall("this ([a-z]+)", text)
    return nouns

def find_pronouns(text):
    pronouns = re.findall(" he | his ", text)
    pronouns = pronouns + re.findall(" she | her ", text)
    pronouns = pronouns + re.findall(" they | them ", text)
    pronouns = pronouns + re.findall(" its ", text)

    clean_pronouns = []
    for i in pronouns:
        clean_pronouns = clean_pronouns + [i.strip()]
    
    return clean_pronouns
    


if __name__ == "__main__":

    
    #text = "this nations continuation_war involved an alliance with germany partially to respond to a neighbors use of the aland islands and ended during gustaf mannerheims presidency. it helped the nazis because it allowed for submarine training in the baltic and cut off the murmansk railroad. this followed a 4 month war with fighting was over control of the petsamo mines lake_ladoga and the the karelian isthmus called the winter_war."
    #text = "this group 's power peaked in the 31st congress when two senators and 14 representatives claimed membership. formed after the barnburner democrats split from the main party it was absorbed into the republican party."
    #text = "in 1866 this mans nation under the command of his consul henri bellonet attempted to occupy the korean island of ganghwa and in another part of the world he freed the algerian leader abd al qadir."
    text = "the founder of this empire had been a governor under diodotus. its earliest capital was at dara and later moved to hecatompylos. it was eventually overrun by the sassanids who took its city of ctesiphon for their own capital. conquered in 226 a.d. by artaxerxes it had existed for almost 500 years from when arsaces i liberated it from the seleucid turks in 247 bc."
    #text = "this president vetoed the texas seed bill and controversially proposed the return of confederate flags held by the war department."
    
    links = find_links(text)
    print links

    nouns = find_this_nouns(text)
    print nouns

    pronouns = find_pronouns(text)
    print pronouns

    print " ".join(links + nouns + pronouns)

