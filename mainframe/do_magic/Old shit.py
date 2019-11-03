# Separates nouns from nonNouns.  Parses table for match.
    # for word in tagged_sentence:
    #     if word[1] == "NNP":
    #         nouns.append(word[0])
    #         category = "Person"
    #     elif word[1] == "NN":
    #         nouns.append(word[0])
    #         words.append(word[0])
    #     else:
    #         words.append(word[0])

    # searches for word in look up table.
    # wordList = voila.get_stopwords(words)

    # for word in wordList:
    #     phrase_result = sqlQuery.dbQuery("select * from phrase join lookup_table as LU on phrase.FK=LU.PK where Phrase"
    #                                      " like " + "'%" + word + "%'")
    #     if phrase_result:
    #         wordResults.append(phrase_result)
    #     else:
    #         nonMatchedWord.append(word)

    # begins triangulation of all words (non proper nouns) from lookup table.
    # wordResults = answer.triangulate(wordResults)

    # if no results check for wordnet hits and triangulates.
    # if len(wordResults) == 0:
    #     wordResults = answer.triangulate(wordNetResults(nonMatchedWord))
    #
    # # ensures correct form of the
    # if len(wordResults) > 1:
    #     results = answer.triangulate(breakTie(nonMatchedWord))
    #     if len(results) > 0:
    #         wordResults.append(results)
    #     wordResults = answer.triangulate(wordResults)
    #
    # if len(wordResults) > 0:
    #     while isinstance(wordResults[0], tuple):
    #         wordResults = answer.flatten(wordResults)

    # todo insert check here to validate wordresults isn't empty
    # if this is empty you can run candidates, then start looking at "bad returns".

    # sets basic SQL begining
    # selectStatment = "select * from player_data where name like "
    #
    # for table in tableList:
    #     if table == wordResults[5]:
    #         selectStatment = "select * from " + table + " where LOWER(name) LIKE LOWER"
    #
    # # searches for direct name look up from table returned from non-noun check.
    # for noun in nouns:
    #     result = sqlQuery.dbQuery(selectStatment + "('%" + noun + "%') ")
    #     if result:
    #         playerResults.append(result)
    #     else:
    #         nonMatchedWord.append(noun)
    #
