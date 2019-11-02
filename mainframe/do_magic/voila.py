# created to clean up main

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from spellchecker import SpellChecker
from nltk.tag import StanfordPOSTagger
from nltk.stem import WordNetLemmatizer

counter = y = 0
check = SpellChecker()


def tag_Sentence(tokenized):
    import os
    jarpath = "C:/Program Files/Java/jdk-11.0.2/bin/java.exe"
    java_path = jarpath
    os.environ['JAVAHOME'] = java_path

    dirname = os.path.dirname(__file__)
    jar = os.path.join(dirname, '../../stanford-postagger-full-2018-10-16/stanford-postagger-3.9.2.jar')
    model = os.path.join(dirname, '../../stanford-postagger-full-2018-10-16/models/english-left3words-distsim.tagger')

    stanfordPOS = StanfordPOSTagger(model, jar, encoding='utf-8')
    #print(f'tokenized words:    {tokenized}')
    # begin pos tagging
    postaggedwords = stanfordPOS.tag(tokenized)
    #print(f'these are tagged words:      {postaggedwords}')

    return postaggedwords


def spell_check(tokenized):
    # begin spell check  This is causing more harm than good right now
    # spellchecks 1 word at a time so no need for loop
    spelledWords = check.correction(tokenized)
    # spellcheck 'worked'
    if spelledWords != tokenized:
        print(f'did you mean, {spelledWords}?')
        inputval = input('[y/N]: ')
        if inputval == 'y':
            return spelledWords
        else:
            # lets go another route and find some other matches
            candidates = check.candidates(tokenized)
            if len(candidates) > 1:
                for i, candidate in enumerate(candidates):
                    print(f'[{i}]   [{candidate}]')
                #     if yes to any of these then we return this and run a db query on this
                print(f'[{len(candidates)}]   [None]')
                val = int(input('here are some more options, please choose one: '))
                if val >= len(candidates):
                    return
                to_list = list(candidates)
                return to_list[val]
    else:
        return tokenized


def get_basewords(tokenized):
    # begin baseing
    getBase = WordNetLemmatizer()
    # getBase =
    baseWords = []
    for word in tokenized:
        baseWords.append(getBase.lemmatize(word))

    return baseWords


def get_stopwords(tokenized):
    # stopwords

    stop_words = set(stopwords.words('english'))
    _stopwords = [words for words in tokenized if not words in stop_words]
    #print(f'stop words to check for:    {_stopwords}')
    # End getting stop words.

    #
    return _stopwords


# this will be used later to measure our stastics on how accurate our program performs
def runstat():
    global counter, y
    # fyi apparently counter++ is not a thing in python lol
    counter += 1
    value = input('Was this helpful? [y/N]: ')
    if value == 'y':
        y += 1
        return print(f'percentage accurate: {float(y / counter)}')


# todo have not used this yet, may not need but leave it as is.
def one_array(array):
    one = []
    for i in array:
        if isinstance(i, list):
            one_array(i)
        else:
            one.append(i)
    return one


# checks if theres an apostrophe e.g. D'angelo. Adds apostrophe for escape character in SQL --> d''angelo.
# if there is NO apostrophe then returns word
# todo this has helped tremendously
def singlequoteSQLfix(val):
    index = val.find("'")
    return val[:index] + "''" + val[index + 1:] if index != -1 else val

# modifies the query values to make them sql safe search.. eg: d'angelo 3's
def apostrophefix(words):
    for i, word in enumerate(words):
        if i >= len(words) - 1:
            break
        j = i + 1
        # case where three's splits into [three] & ['s], we make it one word [three's] and add the apostrophe to it ->
        # [three''s] for sql safe search. then we remove the tuple ('s, POS) and return ("three''s", "null")
        if words[j][1] == "POS" and words[i][1] == "NN" or words[j][1] == "POS" and words[i][1] == "CD":
            concat = words[i][0] + words[j][0]
            concat = singlequoteSQLfix(concat)
            words[i] = (concat, "null")
            words.remove(words[j])
        else:
            # if the above is not the case e.g d'angelo. just fix it --> d''angelo and return it along with its part of
            # speech
            words[i] = (singlequoteSQLfix(words[i][0]), words[i][1])
    # case where o'neal is last in the query --> o''neal
    # if last value -> [three''s] already has been modified then skip. but for cases where o'neal is last . make it
    # o''neal
    if words[len(words) - 1][0].find("''") == -1:
        words[len(words) - 1] = singlequoteSQLfix(words[len(words) - 1][0]), words[len(words) - 1][1]
    return words