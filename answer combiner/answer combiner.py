from collections import defaultdict
from csv import DictReader, DictWriter
from operator import itemgetter

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

def top_guess(guesses):
    for jj in guesses.split(", "):
        key, val = jj.split(":")
        break
    return key

def guess_score_dict(guesses):
    """
    returns a dictionary of ([guess] = value) of all guess
    """
    d = defaultdict(float)
    for jj in guesses.split(", "):
        key, val = jj.split(":")
        d[key.strip()] = float(val)
    
    return d

WRITE_FILE = 1
USE_TRAIN = 1
NORMALIZE_OUTPUT_SCORE = 1
# alpha value has been optimized to give best rate on training = 0.751838235294
# best found alpha = 0.3
# different alphas for QANTA and IR_Wiki have not been tried
# and would probably be expected to do better
alpha = 0.3 

if __name__ == "__main__":

    if USE_TRAIN:
        print "going with training data"
        #data = DictReader(open("../trainGOOD.csv", 'r'))
        data = DictReader(open("../csv/train.csv", 'r'))
        #data = DictReader(open("../train_SS3.csv", 'r'))
        outfile_name = "train Combined Scores.csv"
        correct_choice = 0
        answer_in = 0
        answer_out = 0
        Q_right = 0
        IR_right = 0
        
    else:
        print "going with test data"
        data = DictReader(open("../csv/test.csv", 'r'))
        outfile_name = "test Combined Scores.csv"

    if WRITE_FILE:
        # Create File for combined scores
        outfile = open(outfile_name, 'w')
        o = DictWriter(outfile, ['Question ID','Sentence Position','Scores'], lineterminator='\n')
        o.writeheader()
    

    guess_count = 0
    guess_count2 = 0
    data_examples = 0
    for ii in data:
        data_examples += 1

        join_d = defaultdict(float)

        Q_d = guess_score_dict(ii['QANTA Scores'])
        IR_d = guess_score_dict(ii['IR_Wiki Scores'])

        Q_sum = 0
        IR_sum = 0

        for key in Q_d.keys():
            #print key, Q_d[key]
            join_d[key] = 1
            Q_sum += Q_d[key]

        for key in IR_d.keys():
            #print key, IR_d[key]
            join_d[key] = 1
            IR_sum += IR_d[key]

        if Q_sum == 0 or IR_sum == 0:
            print "BAD SUM on question", ii['Question ID']

        Q_sum += 20*alpha
        IR_sum += 20*alpha

        if Q_sum == 0 or IR_sum == 0:
            print "BAD SUM on question", ii['Question ID'], Q_sum, IR_sum

        for key in join_d.keys():
            guess_count += 1
            join_d[key] = ((Q_d[key]+alpha)/Q_sum)*((IR_d[key]+alpha)/IR_sum)

        join_list = join_d.items()
        # sort the list big to small based on 2nd element:
        join_list = sorted(join_list, key=itemgetter(1), reverse=True)

        if NORMALIZE_OUTPUT_SCORE:
            s_sum = 0
            for (g,s) in join_list:
                s_sum += s
            for i in range(len(join_list)):
                (g,s) = join_list[i]
                s /= s_sum
                join_list[i] = (g,s)

        if USE_TRAIN:
            g,s = join_list[0]
            if g == ii['Answer']:
                #print "RIGHT"
                correct_choice += 1
            just_a = [g for g, s in join_list]
            if ii['Answer'] in just_a:
                answer_in += 1
            else:
                answer_out += 1

            if ii['Answer'] == top_guess(ii['QANTA Scores']):
                Q_right += 1
            if ii['Answer'] == top_guess(ii['IR_Wiki Scores']):
                IR_right += 1
                            
        out_line = ""
        for g,s in join_list:
            guess_count2 += 1
            #print g
            if join_list.index((g,s)) == 0:
                out_line += g+":"+str(s)
            else:
                out_line += ", "+g+":"+str(s)

        #print out_line
        
        if WRITE_FILE:
            o.writerow({'Question ID': ii['Question ID'], 'Sentence Position': ii['Sentence Position'], 'Scores': out_line})

    if USE_TRAIN:
        rate = float(correct_choice)/data_examples
        print "correct rate:", rate, ("" if rate < 0.75 else "Good Show")
        print "answer available", float(answer_in)/data_examples
        print "answer not available", float(answer_out)/data_examples
        print "QANTA rate", float(Q_right)/data_examples
        print "IR rate", float(IR_right)/data_examples

    if WRITE_FILE:    
        outfile.close()    
        print "wrote", data_examples, "lines"
        print "wrote", guess_count, "guesses"
        print "wrote2", guess_count, "guesses"
    else:
        print "DONE", data_examples
    
