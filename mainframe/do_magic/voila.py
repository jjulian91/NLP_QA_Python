# created to clean up main

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from spellchecker import SpellChecker
from nltk.tag import StanfordPOSTagger

counter = y = 0

def tag_Sentence(tokenized):
    import os
    jarpath = "C:/Program Files/Java/jdk-11.0.2/bin/java.exe"
    java_path = jarpath
    os.environ['JAVAHOME'] = java_path

    dirname = os.path.dirname(__file__)
    jar = os.path.join(dirname,'../../stanford-postagger-full-2018-10-16/stanford-postagger-3.9.2.jar')
    model= os.path.join(dirname,'../../stanford-postagger-full-2018-10-16/models/english-left3words-distsim.tagger')

    stanfordPOS = StanfordPOSTagger(model, jar, encoding='utf-8')
    print(f'tokenized words:    {tokenized}')
    #begin pos tagging
    postaggedwords = stanfordPOS.tag(tokenized)
    print(f'these are tagged words:      {postaggedwords}')

    return postaggedwords

def spell_check(tokenized):
    #begin spell check  This is causing more harm than good right now
    check = SpellChecker()
    spelledWords = []
    for word in tokenized:
        spelledWords.append(check.correction(word))
    print(f'These are words corrected:  {spelledWords}')

    return spelledWords

def get_basewords(tokenized):
    #begin baseing
    getBase = PorterStemmer()
    baseWords = []
    for word in tokenized:
        baseWords.append(getBase.stem(word))
def get_stopwords(tokenized):
    #stopwords

    stop_words = set(stopwords.words('english'))
    _stopwords = [words for words in tokenized if not words in stop_words]
    print(f'stop words to check for:    {_stopwords}')
    # End getting stop words.

    #
    return _stopwords


# this will be used later to measure our stastics on how accurate our program performs
def runstat():
    global counter, y
    # fyi apparently counter++ is not a thing in python lol
    counter+=1
    value = input('Was this helpful? [y/N]: ')
    if value == 'y':
        y+=1
        return print(f'percentage accurate: {float(y/counter)}')

