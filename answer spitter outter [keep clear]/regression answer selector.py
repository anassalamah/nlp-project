
from csv import DictReader, DictWriter
from collections import defaultdict

## BEGIN ##

infile_name = "../linear regressor/test_guesses_POLYLINE_W3_augment.csv"
data = DictReader(open(infile_name, 'r'))

outfile_name = "regression answers.csv"
outfile = open(outfile_name, 'w')
o = DictWriter(outfile, ['Question ID','Answer'], lineterminator='\n')
o.writeheader()

num_answers_written = 0
current_Q_ID = 0
best_guess = ""
best_score = 0
for ii in data:
    if int(ii['Question ID']) != current_Q_ID and current_Q_ID != 0:
        o.writerow({'Question ID': current_Q_ID, 'Answer': best_guess})
        num_answers_written += 1
        # start a new answer series
        current_Q_ID = int(ii['Question ID'])
        best_guess = ii['Answer']
        best_score = ii['Prob']
    else:
        current_Q_ID = int(ii['Question ID'])
        if ii['Prob'] > best_score:
            best_score = ii['Prob']
            best_guess = ii['Answer']

# write answer for last line
o.writerow({'Question ID': current_Q_ID, 'Answer': best_guess})
num_answers_written += 1

print "wrote", num_answers_written, "lines"
outfile.close()
