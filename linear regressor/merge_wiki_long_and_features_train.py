import sys
from csv import DictReader, DictWriter

if __name__ == "__main__":

    print "sorting and merging wiki_longfeatures_train.csv and features_train.csv"

    # Read in files
    wiki_long= DictReader(open("wiki_longfeatures_train.csv", 'rU'))
    features_train_file = open("features_train.csv", 'rU')
    features_train = DictReader(features_train_file)
    
    # Create a File for output
    outfile = open('wiki_long_features_train_NICK.csv', 'w')
    output = DictWriter(outfile, ['Question ID', 'Sentence Position', 'Answer', 'is correct', 'Q score','IR score','join score', 'category','Wikipedia Score', 'Wikipedia Found', 'SearchWords','SearchFound', 'WikipediaLen'], lineterminator='\n')
    output.writeheader()

    numout = 0

    for bb in features_train:
        print bb['Answer']
        for ii in wiki_long:
            print (ii['Question ID'],ii['Sentence Position'],ii['Answer']), ( bb['Question ID'],bb['Sentence Position'],bb['Answer'])
            #if (ii['Question ID'],ii['Sentence Position'],ii['Answer']) == ( bb['Question ID'],bb['Sentence Position'],bb['Answer']):
            if ii['Question ID'] == bb['Question ID'] and ii['Sentence Position'] == bb['Sentence Position'] and ii['Answer'] == bb['Answer']: 
                numout += 1
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
                                 'WikipediaLen': ii['WikipediaLen'] })
                break
              
        if numout > 20:
            break
    outfile.close()
    print "done", 'wiki_long_features_train_NICK.csv'
