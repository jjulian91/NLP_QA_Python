import nltk
import do_magic.voila as voila
import do_magic.dataQuery as sqlQuery
import do_magic.answerFinder as answer


def parseQuestion(question):
    tokenized = nltk.word_tokenize(question)
    nonMatchedWord = []  # list of words (NOT NOUNS) which may be used to break ties with spell checker.
    playerResults = []  # list of results generated by noun search.
    wordResults = []  # list of results generated by nonNouns
    statsResults = []
    capturedWords = []

    # remove the pesky "'s" from tokenized, and capture words
    # todo talk about why some of this is commented out? was it moved? We can add the search for max or min (or similar)
    #  then we can start looking at pulling out things which will be applied to all functions and what is only applied to
    #  specific cases.  and only have to create some small changes and still use the rest of the information which was
    #  already defined for the most of the project.
    for word in tokenized:
        # if word.lower() == ("where" or "when"): #may need to expand on these.
        #     capturedWords.append(word)
        # if word.isnumeric():
        #     capturedWords.append(word)
        if "\'" in word:
            tokenized.remove(word)

    # DONE DO NOT MODIFY
    tokenized = voila.get_stopwords(tokenized)
    tokenized = voila.get_basewords(tokenized)
    voila.addToList(tokenized, capturedWords)
    raw_input_as_last_option = ''
    for word in tokenized:
        result = sqlQuery.search_phrase_DB(word)
        if result:
            voila.addToList(wordResults, result)
            raw_input_as_last_option = raw_input_as_last_option + word + ' '
        else:
            result = sqlQuery.search_player_dB(word)
            result_stat = sqlQuery.search_stats_DB(word)
            if result:
                voila.addToList(playerResults, result)
            if result_stat:
                voila.addToList(statsResults, result_stat)
            else:
                nonMatchedWord.append(word)
    # END DONE DO NOT MODIFY
    raw_input_as_last_option = raw_input_as_last_option.strip()
    year = voila.check_for_year(tokenized)
    tableName = "placeholder"
    playerName = "placeholder"

    wordResults = answer.processResults(wordResults, nonMatchedWord)  # processResults begins triangulation.
    # process results returns a tuple or list, if tuple we have triangulate, if not we have multiple entires.
    print(wordResults)
    if isinstance(wordResults, tuple):
        tableName = voila.singlequoteSQLfix(wordResults[5])
    else:
        wordResults = raw_input_to_N_tuples(raw_input_as_last_option, wordResults)
        if isinstance(wordResults, tuple):
            tableName = voila.singlequoteSQLfix(wordResults[5])
        # return "there were multiple hits for your query please limit query to only one field or stat at a time"

    if tableName == "player_data":
        playerResults = answer.processResults(playerResults, nonMatchedWord)  # processResults begins triangulation.
        if isinstance(playerResults, tuple):
            playerName = voila.singlequoteSQLfix(playerResults[0])
        else:
            return playerResults

    if tableName == "stats":
        statsResults = answer.processResults(statsResults, nonMatchedWord)  # processResults begins triangulation.
        if year:
            statsResults = answer.find_with_year(year, statsResults)
        if isinstance(statsResults, tuple):
            playerName = voila.singlequoteSQLfix(statsResults[0])
            #     THE CONNECTION GOES HERE
            index_for_answer = wordResults[4]
            return statsResults[index_for_answer]
        else:
            #todo this is where we need to do the "most recent entry"
            return statsResults

    return_info = answer.return_tablename_with_player_name(wordResults, playerName)

    if return_info == 0:
        return "unable to find match"

    return return_info


def raw_input_to_N_tuples(string, list_of_tuples):
    for row in list_of_tuples:
        if row[0] == string:
            return row
