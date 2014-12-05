NLP-Project
===========
Members: Anas Salamah, Jordan Hoskins, Nick Farrow

Project Proposal: https://docs.google.com/document/d/1x34VXmbU3Hr0deV65aqz5kN6jJbPxMDYg72f9zURHZw/edit?usp=sharing

TODO List
===========

* [DONE] clean answers based on Question pronouns (?) see below open request

* [DONE] read training/test files, and extract the question sentences, and return the clean sentences.
(sentences returned as a python list, no period exists at end of sentence, all lowercase letters)
(python code for this in minimal examples folder)

* [DONE] Write code to evaluate the QANTA and IR_Wiki guessers performance.
Create an initial guess (solution file) based on the top computer guesses only.
No sentence information will be used for this initial guess, Naive Bayes is used instead.
(code for this in bayes classifier example)

* [DONE] Submit a first guess to Kaggle

* [DONE] Collect wikipedia articles

* [NICK] Break Wikipedia articles into separate pages

* [JORDAN] Take a question text block and identify all interesting words for the bag-of-words match

* [OPEN] Take a list of words and a wikipeida article, return a SCORE for the article based on the words

* [OPEN] Figure out if the question text block is asking about a person

* [OPEN] Verify that the list of pronouns we are checking is an complete (exhaustive) list

Refactor Requests
===========

* [ANAS] make a new .csv of all wikipeida links tagged by name (yes/no) from freebase to use as look-up file
* [ANAS] change remove_none_types to use a .csv for name look ups
 