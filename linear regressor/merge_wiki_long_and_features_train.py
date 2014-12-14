import sys
from csv import DictReader, DictWriter

if __name__ == "__main__":

    print "sorting and merging wiki_longfeatures_train.csv and features_train.csv"

    # Read in files
    wiki_long= DictReader(open("wiki_longfeatures_train.csv", 'rU'))
    features_train_file = open("features_train.csv", 'rU')
    features_train = DictReader(features_train_file)
    
    # Create a File for output
    output = DictWriter(open('wiki_long_features_train.csv', 'w'), ['Question ID', 'Sentence Position', 'Answer', 'is correct', 'Q score','IR score','join score', 'category','Wikipedia Score', 'Wikipedia Found', 'SearchWords','SearchFound', 'WikipediaLen'], lineterminator='\n')
    output.writeheader()
    count = 0
    for ii in wiki_long:
    	count += 1
    	print count
        for bb in features_train:
            #print bb
            if (ii['Question ID'],ii['Sentence Position'],ii['Answer']) == ( bb['Question ID'],bb['Sentence Position'],bb['Answer']):
                output.writerow({'Question ID': ii['Question ID'], \
                                     'Sentence Position': ii['Sentence Position'], \
                                     'Answer': ii['Answer'], \
                                     'is correct': bb['is correct'], \
                                     'Q score': bb['Q score'], \
                                     'IR score': bb['IR score'], \
                                     'join score': bb['join score'], \
                                     'category': bb['category'], \
                                     'Wikipedia Score': ii['Wikipedia Score'], \
                                     'Wikipedia Found': ii['Wikipedia Found'], \
                                     'SearchWords': ii['SearchWords'], \
                                     'SearchFound': ii['SearchFound'], \
                                     'WikipediaLen': ii['WikipediaLen'] })
                break;
        features_train_file.seek(0)
                #print "MATCH: ", ii['Question ID'], ii['Sentence Position'], ii['Answer'], bb['Q score'], bb['IR score'], bb['join score'],bb['category'],ii['Wikipedia Score'],ii['Wikipedia Found'],ii['SearchWords'],ii['SearchFound'],ii['WikipediaLen']
                #print ''

    
