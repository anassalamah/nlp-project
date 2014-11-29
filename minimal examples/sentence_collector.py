from csv import DictReader, DictWriter

def split_question_sents(text, num_expected):
    """
    takes the question text and returns it as a list of clean sentences
    a sentence is a list of lowercase chars and symbols that has no whitespace at the beginning and end
    there is no period at the end of the sentence
    """
    sents = []
    for s in text.split("."):
        sents.append(s.strip())

    # in most (all?) cases, there will be an empty element addded at the end (something after the . ?)
    del sents[-1]   # cleans up the empty entry

    if len(sents) != num_expected:
        print "ERROR, num sentences is unexpected"

    return sents


if __name__ == "__main__":

    # Read in test/train data
    data = DictReader(open("../test.csv", 'r')) 
    
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

    for ii in data:
        text = ii['Question Text']
        num_sents = int(ii['Sentence Position']) + 1
        sents = split_question_sents(text, num_sents)
        for jj in sents:
            print jj    # prints cleaned sentences one line at a time

        print ""        # print blank line between seperate questions
        
