# created to clean up main

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from spellchecker import SpellChecker
from nltk.tag import StanfordPOSTagger

counter = y = 0

def word_Magic(question):
    import os
    jarpath = "C:/Program Files/Java/jdk-11.0.2/bin/java.exe"
    #
    #jarpath = "put path here"
    java_path = jarpath
    os.environ['JAVAHOME'] = java_path

    jarpath = 'C:/Users/jonju/Documents/NLP_QA_Python/stanford-postagger-full-2018-10-16/stanford-postagger-3.9.2.jar'
    #jarpath=""

    modelpath='C:/Users/jonju/Documents/NLP_QA_Python/stanford-postagger-full-2018-10-16/models/english-left3words-distsim.tagger'
    #modelpath=""

    jar = jarpath
    model = modelpath
    stanfordPOS = StanfordPOSTagger(model, jar, encoding='utf-8')
    #check = SpellChecker()
    getBase = PorterStemmer()
    tokenized = nltk.word_tokenize(question)
    baseWords = []
    for word in tokenized:
        baseWords.append(getBase.stem(word))
    spelledWords = []
    # for word in baseWords:
    #    spelledWords.append(check.correction(word))
    print(f'tokenized words:    {baseWords}')
    # gives us stop words to run part of
    # speech on to begin categorization.
    #
    # Stop Words may not be necessary
    #
    #
    stop_words = set(stopwords.words('english'))
    _stopwords = [words for words in baseWords if not words in stop_words]
    print(f'stop words to check for:    {_stopwords}')
    # End getting stop words.
    postaggedwords = stanfordPOS.tag(baseWords)
    #print(f'these are tagged words:      {postaggedwords}')
    return postaggedwords


# this will be used later to measure our stastics on how accurate our program performs
def runstat():
    global counter, y
    # fyi apparently counter++ is not a thing in python lol
    counter+=1
    value = input('Was this helpful? [y/N]: ')
    if value == 'y':
        y+=1
        return print(f'percentage accurate: {float(y/counter)}')

