from nltk.tokenize import word_tokenize
from csv import DictReader, DictWriter

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

def clean_guesses(guesses, pronoun):
    """
    return a string that only has the guesses relative to its type

    """
    if not pronoun:
        print "PRONOUNS EMPTY, returning guesses as is" 
        return guesses
    elif pronoun in person_pronouns:
        # Read in person INFO
        answer_info_file = open("../csv/person_info.csv", 'r')
        answer_info = DictReader(answer_info_file)
    else:
        # Read in non_person NER
        answer_info_file = open("../csv/non_person_info.csv", 'r')
        answer_info = DictReader(answer_info_file)
    new_guesses= ""
    top_mismatch = 0
    # insert bool to know if top key matches any of the answers in the relative csv file
    found_key = False
    for jj in guesses.split(", "):
        #print jj
        key,val = jj.split(":")
        for ii in answer_info:
            if key == ii["Answer"]:
                found_key = True
                new_guesses += jj+", "
        if not found_key:
            top_mismatch += 1
            print "TOP GUESS NOT OF PRONOUN TYPE", top_mismatch
            # if the top 5 guesses are not of the estimated answer csv file,
            # then return the original guess
            if top_mismatch >= 5:
                return (guesses, top_mismatch)
        #reset CSV iterator
        answer_info_file.seek(0)
    #print "MOST COMMON PRONOUN : ", pronouns
    #print "CLEANED GUESSES :", new_guesses
    #print "OLD GUESSES :", guesses
    #print ""
    """ remove last ', ' """
    new_guesses = new_guesses[:-2]
    print new_guesses
    return (new_guesses, top_mismatch)

if __name__ == "__main__":
    
    print "read training data answer"
    
    # Read in training data
    train = DictReader(open("../csv/train.csv", 'rU'))
    
    # Create File for predictions
    output = DictWriter(open('Q-info-train.csv', 'w'), ['Question ID', 'Sentence Position', 'Answer', 'Pronouns','Top Pronoun','Top Q Mismatch', 'Clean Q Scores','Top IR Mismatch', 'Clean IR Scores', 'category'], lineterminator='\n')
    output.writeheader()
    
    answer_counts = 0
    
    for ii in train:
        pronouns = find_pronouns(ii["Question Text"])
        pronoun = most_common_pronoun(pronouns)
        if pronoun:
            Q_clean_text, Q_top_mismatch = clean_guesses(ii["QANTA Scores"], pronoun)
            IR_clean_text, IR_top_mismatch = clean_guesses(ii["IR_Wiki Scores"], pronoun)
            output.writerow({'Question ID': ii['Question ID'], \
                        'Sentence Position': ii['Sentence Position'], \
                        'Answer': ii['Answer'], \
                        'Pronouns' : pronouns, \
                        'Top Pronoun': pronoun, \
                        'Top Q Mismatch': Q_top_mismatch,
                        'Clean Q Scores': Q_clean_text, \
                        'Top IR Mismatch': IR_top_mismatch,
                        'Clean IR Scores': IR_clean_text, \
                        'category': ii['category']})
        else:
                       output.writerow({'Question ID': ii['Question ID'], \
                        'Sentence Position': ii['Sentence Position'], \
                        'Answer': ii['Answer'], \
                        'Pronouns' : "", \
                        'Top Pronoun': "", \
                        'Top Q Mismatch': "",
                        'Clean Q Scores': "", \
                        'Top IR Mismatch': "",
                        'Clean IR Scores': "", \
                        'category': ii['category']})
                           
                               
