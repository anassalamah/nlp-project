import nltk
from nltk.corpus import stopwords
from csv import DictReader, DictWriter

train = DictReader(open('train_SS3.csv', 'r'))
"""for ii in train:
    for w in ii['Question Text']:
        if not w in stopwords.words('english'):
            ' '.join(w)
            print w
#print stopwords.words('english')
"""
for ii in train:
    print ii['Question Text']
