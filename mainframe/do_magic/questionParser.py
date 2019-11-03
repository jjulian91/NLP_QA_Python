import nltk
import do_magic.voila as voila
import do_magic.dataQuery as sqlQuery
import do_magic.answerFinder as answer
from nltk.corpus import wordnet

tableList = ["phrase", "player_data", "stats"]


# return from this statement " ("select * from phrase join lookup_table as LU on phrase.FK=LU.PK where Phrase like "
#              + "'%" + word + "%'") "
# is : [('tall', 56, 56, 'height', 5, 'player_data')]
# 0 = reference 1 = FK 2 = PK 3 = name of column 4 = column number (for getting answer). 5 is table where lookup is found
# also for building SQL statement when getting answer.

# todo I finished general triangulation used wordnet to check stop words after spell check after lookup table.  There is
#   a new DB dump -- fix the insert statement first using weight before trying to upload the new DB tables. This will
#    a wider range of items you can test the insert statment on to verify it is correctly inserting. then we can use
#     just a bunch of questions to "train" this model and insert the words by asking questions.  this way we use as little
#      human interaction as possible (meaning less calls to candidates) so its a more "automated" system.
# https://www.geeksforgeeks.org/get-synonymsantonyms-nltk-wordnet-python/
# todo capture dates/year ex: how many points did larry bird have in 1971?

def parseQuestion(question):
    tokenized = nltk.word_tokenize(question)
    nonMatchedWord = []  # list of words (NOT NOUNS) which may be used to break ties with spell checker.
    playerResults = []  # list of results generated by noun search.
    wordResults = []  # list of results generated by nonNouns
    statsResults = []
    tokenized = voila.get_stopwords(tokenized)
    tokenized = voila.get_basewords(tokenized)
    for word in tokenized:
        if search_phrase_DB(word):
            wordResults = search_phrase_DB(word, wordResults)

        elif search_player_dB(word):
            playerResults = search_player_dB(word, playerResults)
        elif search_stats_DB(word):
            statsResults = search_stats_DB(word, statsResults)
        else:
            nonMatchedWord.append(word)
    category = "unknown"  # could be used for flag info or not whatever

    if wordResults:
        # todo why processResults on this??? when processresults it empties the array. made this instead
        answer.reemovNestings(wordResults)
        wordResults = answer.get_output()
        wordResults = answer.remove_single_tuple_within_list(wordResults)
        answer.reset_output()
        # wordResults = processResults(wordResults, nonMatchedWord)
    if playerResults:
        playerResults = processResults(playerResults, nonMatchedWord)
        answer.reemovNestings(playerResults)
        playerResults = answer.get_output()
        playerResults = answer.remove_single_tuple_within_list(playerResults)
        answer.reset_output()
    if statsResults:
        statsResults = processResults(statsResults, nonMatchedWord)
    # todo this is the start of the switch statements I believe -- each case would require a different

    if playerResults:
        playerName = voila.singlequoteSQLfix(playerResults[0])
    elif statsResults:
        playerName = voila.singlequoteSQLfix(statsResults[0])

    return_info = return_tablename_with_player_name(wordResults, playerName)
    return return_info


def return_tablename_with_player_name(wordResults, playerName):
    tableName = voila.singlequoteSQLfix(wordResults[5])
    finalAnswer = list(answer.flatten(
        sqlQuery.dbQuery("select * from " + tableName + " where name =" + "'" + playerName + "'")))
    finalAnswer = list(finalAnswer[0])
    finalIndex = wordResults[4]
    return finalAnswer[finalIndex]


def breakTie(nonMatched):
    nonMatched = voila.get_stopwords(nonMatched)
    searchMatch = []
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
                        searchMatch.append(result)
    return searchMatch


# todo test the insert statement.  The idea is that if a lemma gets a match we add the word which the lemma
# was derived from to the phrase table with the PK found by the lemma.  This will reduce the number of calls to this
#  function so that we don't have this terrible o(n^3) function called more than it needs to be.
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


def search_player_dB(word, nameResults):
    result = sqlQuery.dbQuery(
        "select * from player_data where LOWER(name) LIKE LOWER ('%" + word + "%')")
    if result:
        addToList(nameResults, result)

    return nameResults


def search_stats_DB(word, statResults):
    result = sqlQuery.dbQuery(
        "select * from stats where LOWER(name) LIKE LOWER ('%" + word + "%')")
    if result:
        addToList(statResults, result)
    return statResults

def search_phrase_DB(word, wordResults):
    result = sqlQuery.dbQuery("select * from phrase join lookup_table as LU on phrase.FK=LU.PK where Phrase"
                              " like " + "'%" + word + "%'")
    if result:
        addToList(wordResults, result)

    return wordResults


def processResults(playerResults, nonMatchedNouns):
    playerResults = answer.triangulate(playerResults)

    if len(playerResults) > 0 and not isinstance(playerResults[0], list):
        results = answer.triangulate(breakTie(nonMatchedNouns))
        if len(results) > 0:
            playerResults.append(results)
            playerResults = answer.triangulate(playerResults)
    playerResults = list(answer.flatten(playerResults))
    return playerResults

def addToList(resultsList, results):
    for result in results:
        resultsList.append(result)