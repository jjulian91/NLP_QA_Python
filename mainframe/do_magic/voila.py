# created to clean up main

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from spellchecker import SpellChecker

counter = y = 0

def word_Magic(question):
    check = SpellChecker()
    getBase = PorterStemmer()
    tokenized = nltk.word_tokenize(question)
    baseWords = []
    for word in tokenized:
        baseWords.append(getBase.stem(word))
    spelledWords = []
    for word in baseWords:
        spelledWords.append(check.correction(word))
    print(f'tokenized words:    {spelledWords}')
    # gives us stop words to run part of
    # speech on to begin categorization.
    #
    # Stop Words may not be necessary
    #
    #
    stop_words = set(stopwords.words('english'))
    _stopwords = [words for words in spelledWords if not words in stop_words]
    print(f'stop words to check for:    {_stopwords}')
    # End getting stop words.
    postaggedwords = nltk.tag.stanford.StanfordPOSTagger(spelledWords)
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

