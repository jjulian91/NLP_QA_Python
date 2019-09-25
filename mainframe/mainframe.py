import nltk
from nltk.corpus import stopwords
# DIFFERENT WAY OF IMPORTING
# from nltk import tokenize
# tokenize.sent_tokenize
counter = y = 0

def main():
    
    while(1):
        category = "blank"
        value = input('Enter in a question: ')
        tagged_sentence = word_Magic(value)
        print(tagged_sentence)
        for words in tagged_sentence:
            if words[1] == "NNP" or words[1] == "NNPS":
                category = "Name"
            elif words[1] == 'WP' or words[1] == "WP$":
                category = "Person"
            elif words[1] == "WRB" or words[1] == "WDT":
                category = "Location"
        print(category)
        runstat()

# this will be used later to measure our stastics on how accurate our program performs
def runstat():
    global counter, y
    # fyi apparently counter++ is not a thing in python lol
    counter+=1
    value = input('Was this helpful? [y/N]: ')
    if value == 'y':
        y+=1
        return print(f'percentage accurate: {float(y/counter)}')
        
def check_stopwords(tokenized):
    filtered = []
    # pulled from nltk website
    stopWords = set(stopwords.words('english')) 
    for words in tokenized:
        if words not in stopWords:
            filtered.append(words)
    return print(f'sentence with removed stop-words:  {filtered}')

#     for list of tested stop words . REMOVE AFTER YOU SEE THIS.
# https://www.geeksforgeeks.org/removing-stop-words-nltk-python/

def word_Magic(question):
    tokenized = nltk.word_tokenize(question)
    print(f'tokenized words:    {tokenized}')
    # gives us stop words to run part of
    # speech on to begin categorization.
    #
    # Stop Words may not be necessary
    #
    #
    stop_words = set(stopwords.words('english'))
    _stopwords = [words for words in tokenized if not words in stop_words]
    print(f'stop words to check for:    {_stopwords}')
    # End getting stop words.
    postaggedwords = nltk.pos_tag(tokenized)
    #print(f'these are tagged words:      {postaggedwords}')
    return postaggedwords

if __name__ == '__main__':
    main()
