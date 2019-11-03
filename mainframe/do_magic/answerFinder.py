import collections
import nltk
import do_magic.voila as voila
import do_magic.dataQuery as sqlQuery
from nltk.corpus import wordnet

output = []
tableList = ["phrase", "player_data", "stats"]
def return_tablename_with_player_name(wordResults, playerName):
    if playerName == "placeholder":
        return 0
    tableName = voila.singlequoteSQLfix(wordResults[5])
    finalAnswer = list(
        sqlQuery.dbQuery("select * from " + tableName + " where name =" + "'" + playerName + "'"))
    finalAnswer = list(finalAnswer[0])
    finalIndex = wordResults[4]
    return finalAnswer[finalIndex]

def triangulate(results):
    overlap = []
    # todo made easier to read loop. old one is in 'OLD SHIT'. once confirmed. delete this line.
    for j in range(len(results)):
        for i in range(j + 1, (len(results))):
            if compareTuples(results[i], results[j]):
                overlap.append(results[j])
    if len(overlap) < 1:
        return False
    else:
        return overlap

def compareTuples(tuple1, tuple2):
    if len(tuple2) != len(tuple1):
        return False
    i = 0
    while(i < len(tuple1)):
        if tuple1[i] == tuple2[i]:
            i += 1
        else:
            return False

    return True

def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes, tuple)):
            yield from flatten(el)
        else:
            yield el

def removeNestings(l):
    for i in l:
        if type(i) == list:
            removeNestings(i)
        else:
            output.append(i)

def breakTie(searchMatch, nonMatched):
    nonMatched = voila.get_stopwords(nonMatched)
    for word in nonMatched:
        # if it already has double quotes that means its ready to be put into sql query and will not go through spellcheck
        if word.find("''") != -1:
            refined_word = word
        # if it doesnt have double quotes run the spell check
        else:
            refined_word = voila.spell_check(word)
            # if spell check returns something back like o'neal. o'neal is NOT sql query safe. so we need to make it o''
            # neal to make it sql query safe
            if refined_word:
                refined_word = voila.singlequoteSQLfix(refined_word)
                for table in tableList:
                    result = sqlQuery.dbQuery("select * from " + table + " where * like " + "'%" + refined_word + "%'")
                    if result:
                        voila.addToList(searchMatch, result)
    return searchMatch

def get_output():
    return output

def reset_output():
    global output
    output = []

def remove_single_tuple_within_list(array):
    if isinstance(array[0], tuple):
        return list(array[0])
    else:
        return array

def processResults(resultArray, nonMatchedNouns):
    if len(resultArray) == 1:
        return resultArray[0]
    elif triangulate(resultArray):
        resultArray = triangulate(resultArray)
    if len(resultArray) > 1:
        results = triangulate(breakTie(resultArray, nonMatchedNouns))
        if results:
            return
    else:
        return resultArray

def wordNetResults(nonMatched):
    results = []
    for word in nonMatched:
        for syn in wordnet.synsets(word):
            for lemmas in syn.lemmas():
                print(f'lemmas: {lemmas.name()}')
                result = sqlQuery.dbQuery("select * from phrase join lookup_table as LU on phrase.FK=LU.PK where Phrase"
                                          " like " + "'%" + lemmas.name() + "%'")
                if result:
                    results.append(result)
                    print(f"INSERT INTO phrase (Phrase, FK) VALUES ({word}, {result[1]})")
                    sqlQuery.dbInsert(f"INSERT INTO phrase (Phrase, FK) VALUES ({word}, {result[1]})")

    return results