from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# DIFFERENT WAY OF IMPORTING
# from nltk import tokenize
# tokenize.sent_tokenize
counter = y = 0

def main():
    
    while(1):
        value = input('Enter in a question: ')
        tokenized = word_tokenize(value)
        print(f'tokenized words:    {tokenized}')
        check_stopwords(tokenized)
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

if __name__ == '__main__':
    main()
