NLP-Project
===========
Members: Anas Salamah, Jordan Hoskins, Nick Farrow

Project Proposal: https://docs.google.com/document/d/1gp4Rewl7RtcmC2mRnU7SY7rK689tZwsBWrUZ2guCPUg/edit

TODO List
===========

* [DONE] read training/test files, and extract the question sentences, and return the clean sentences.
(sentences returned as a python list, no period exists at end of sentence, all lowercase letters)
(python code for this in minimal examples folder)

* [DONE] Write code to evaluate the QANTA and IR_Wiki guessers performance.
Create an initial guess (solution file) based on the top computer guesses only.
No sentence information will be used for this initial guess, Naive Bayes is used instead.
(code for this in bayes classifier example)

* [DONE] Submit a first guess to Kaggle

* [DONE] Collect wikipedia articles

* [DONE] Break Wikipedia articles into separate pages (except for about 50 missing ones, use look up table to find the filename to read for a given guess)


* [DONE] Take a .csv list of all possible answers (wiki_links.csv) and output a new .csv file with a column for PERSON (boolean) based on freebase results
(output is in csv/answer_ner.csv)

* [DONE] Take a .csv list of all possible answers (1) and output two new csv files, person_info.csv and non_person_info.csv, with columns ["Description" (String),"Specific type" (String), "General type (String)] containing summary text output and a domain like ['Morach', 'US President','military Comamander','city','democratic party', 'United States presidential election, 2004',...]"
(output is in csv/person_info.csv and non_person_info.csv)

* [DONE] Verify that the list of pronouns we are checking is complete (exhaustive) list.
(verified and here is the list:
person_pronouns = ['he','him','his','she','her','hers','himself','herself','each other',"each other's", 'one another', "one another's",'who','whoever','whomever','whom','whose'] 
thing_pronouns = ["it", "its", "who"]
group_pronouns= ['they", "them", "their", theirs'])

* [NICK] Take input (1) list of words and (2) wikipedia link guess -> open associated wikipeida article text file, return a SCORE for the article based on if the words from the list appear in the article.

* [ANAS] Take input (1) list of words and (2) description text and domains, return a SCORE (?).

* [JORDAN] Take a question text block and identify all interesting words for the bag-of-words match (e.g. just throw out stopwords), return interesting words as a list.

* [ANAS][ISSUE] Take a question text block and assign a probability of it asking for a PERSON. (figure out from the question text based on pronouns in the text)
(I'm not sure where to put "which","that" in the three categories. I am working on this in (answer NER/answer_ner_compare.py), specifically in find_type_pronoun_probability(pronouns,pronoun_type, vocab_size)
(the reason this is work is in answer NER is because I want to create an output file that can show us both the original answer set and the new one)

Refactor Requests
===========

* [ANAS] make a new .csv of all wikipeida links tagged by name (yes/no) from freebase to use as look-up file. 
(I think this is the same task as "[ANAS] Take a .csv list of all possible answers ...)

* [NICK] figure out which files were affected by previous incomplete list in wiki_links.csv, and add the missing links to the output files (e.g. run missing_links.csv through answer_ner.csv, and append original output files)
 
