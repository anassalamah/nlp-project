from nltk.tokenize import word_tokenize
from csv import DictReader, DictWriter
from collections import defaultdict

# pronouns
person_pronouns = ['he','him','his','she','her','hers','himself','herself','each other',"each other's", 'one another', "one another's",'who','whoever','whomever'] 
thing_pronouns = ["it", "its"]
group_pronouns= ['they", "them", "their", theirs']
all_pronouns = person_pronouns + thing_pronouns + group_pronouns

def find_pronouns(text):
    """
    find the pronouns in a question text
    """
    tokens = word_tokenize(text)
    #print tokens
    pronouns  = []
    for i in tokens:
        if i in all_pronouns:
            pronouns.append(i)
    #print pronouns
    return pronouns

def most_common_pronoun(pronouns):
    """
    return the most common pronoun,
    and in the case of many pronouns having the same count,
    return the first one that appears in the string
    """
    if pronouns:
        pronouns = max(set(pronouns), key= lambda x: (pronouns.count, -pronouns.index(x)))
        
    return pronouns

def guess_score_dict(guesses):
    """
    returns a dictionary of ([guess] = value) of all guess
    """
    d = defaultdict(float)
    for jj in guesses.split(", "):
        key, val = jj.split(":")
        d[key.strip()] = float(val)
    
    return d

def get_type_pronouns(pronons):
    person_pro = []
    thing_pro = []
    group_pro = []
    for i in pronouns:
        if i in person_pronouns:
            person_pro.append(i)
        elif i in group_pronouns:
            group_pro.append(i)
        elif i in thing_pronouns:
            thing_pro.append(i)
    return (person_pro, thing_pro, group_pro)
    

if __name__ == "__main__":
    
    print "read training data answer"
    
    # Read in training data
    train = DictReader(open("../csv/test.csv", 'rU'))
    joined_data = DictReader(open("../answer combiner/train Combined Scores.csv", 'r'))
    
    # Create File for predictions
    """
    index person 0-person_pronouns_lenght
            and then thing rponouns and so on
    """
    output = DictWriter(open('pronouns_feature_test.csv','w'), ['Question ID', 'Sentence Position','Answer','Person pronouns','Thing pronouns','Group pronouns', 'category'], lineterminator='\n')
    #output = DictWriter(open('Q_info_test.csv', 'w'), ['Question ID', 'Sentence Position', 'Pronouns','Top Pronoun','Top Q Mismatch', 'Clean Q Scores','Top IR Mismatch', 'Clean IR Scores', 'category'], lineterminator='\n')
    output.writeheader()
    
    answer_counts = 0
    
    for ii in train:
        answer_counts += 1
        pronouns = find_pronouns(ii["Question Text"])
        person_pronouns,thing_pronouns,group_pronouns = get_type_pronouns(pronouns)
        for bb in joined_data:
            if (ii['Question ID'],ii['Sentence Position'] == bb['Question ID'],bb['Sentence Position']):
                guesses = guess_score_dict(bb['Scores'])
                break
        for key in guesses.keys():
            output.writerow({'Question ID': ii['Question ID'], \
                            'Sentence Position': ii['Sentence Position'], \
                            'Answer': key, \
                            'Person pronouns': len(person_pronouns), \
                            'Thing pronouns' : len(thing_pronouns), \
                            'Group pronouns': len(group_pronouns),\
                            'category': ii['category']})
                           
                               
