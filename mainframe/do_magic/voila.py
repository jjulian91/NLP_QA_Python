import nltk
from nltk.corpus import stopwords
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
    postaggedwords = stanfordPOS.tag(tokenized)
    return postaggedwords


def spell_check(tokenized):
    spelledWords = check.correction(tokenized)
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

def get_most_recent(statresults): #finish implementing
    max = statresults[0]
    for entry in statresults:
        if entry[2] > max[2]:
            max = entry
    return max

def get_basewords(tokenized):
    getBase = WordNetLemmatizer()
    baseWords = []
    for word in tokenized:
        baseWords.append(getBase.lemmatize(word))
    return baseWords


# we can create/delete stop words as we please to better suit our domain.
def get_stopwords(tokenized):
    stop_words = set(stopwords.words('english')) - {type(int), "where", "when"}
    stop_words.add('go' and '?')
    _stopwords = [words for words in tokenized if not words in stop_words]
    return _stopwords


def runstat():
    global counter, y
    counter += 1
    value = input('Was this helpful? [y/N]: ')
    if value == 'y':
        y += 1
        return print(f'percentage accurate: {float(y / counter)}')


def singlequoteSQLfix(val):
    index = val.find("'")
    return val[:index] + "''" + val[index + 1:] if index != -1 else val


def addToList(resultsList, results):
    for result in results:
        resultsList.append(result)


def check_for_year(tokenized):
    for i in range(len(tokenized)):
        if tokenized[i].isdigit():
            if len(tokenized[i]) == 4:
                return tokenized[i]
    else:
        return False
