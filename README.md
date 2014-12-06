NLP-Project
===========
Members: Anas Salamah, Jordan Hoskins, Nick Farrow

Project Proposal: https://docs.google.com/document/d/1x34VXmbU3Hr0deV65aqz5kN6jJbPxMDYg72f9zURHZw/edit?usp=sharing

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

* [JORDAN] Take a question text block and identify all interesting words for the bag-of-words match (e.g. just throw out stopwords), return interesting words as a list.

* [ANAS] Take a .csv list of all possible answers (wiki_links.csv) and output a new .csv file with a column for PERSON (boolean) based on freebase results

* [OPEN] Take input (1) list of words and (2) wikipedia link guess -> open associated wikipeida article text file, return a SCORE for the article based on if the words from the list appear in the article.

* [OPEN] Take a question text block and assign a probability of it asking for a PERSON. (figure out from the question text based on pronouns in the text)

* [ANAS] Verify that the list of pronouns we are checking is complete (exhaustive) list.

* [OPEN] Go through unidentified links file (unidentified_links.csv) and try to correct the guess.  Otherwise, these are the links for which we will not have wikipeida data.

Refactor Requests
===========

* [ANAS] make a new .csv of all wikipeida links tagged by name (yes/no) from freebase to use as look-up file
* [ANAS] change remove_none_types to use a .csv for name look ups
 
