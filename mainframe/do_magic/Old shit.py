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



#     OLD TRIANGULATION

# j = 0
# # todo loop over flattened and check each record for a match of ALL entries in the "tuple"  add those matches to
# # to the overlap function. This should solve 90% of problems going forward.
# while j < len(flattened):
#     i = j + 1
#     while i < len(flattened):
#         k = 1
#         match = True
#         while k < (len(flattened[0])):
#             if flattened[i][k] == flattened[j][k]:
#                 k += 1
#             else:
#                 match = False
#                 break
#
#         if match:
#             overlap.append(flattened[j])
#         i += 1
#     j += 1


## stuff carlos had in question parser:

# if wordResults:
#     # todo why processResults on this??? when processresults it empties the array. made this instead
#     answer.reemovNestings(wordResults)
#     wordResults = answer.get_output()
#     wordResults = answer.remove_single_tuple_within_list(wordResults)
#     answer.reset_output()
#     # wordResults = processResults(wordResults, nonMatchedWord)
# if playerResults:
#     playerResults = processResults(playerResults, nonMatchedWord)
#     answer.reemovNestings(playerResults)
#     playerResults = answer.get_output()
#     playerResults = answer.remove_single_tuple_within_list(playerResults)
#     answer.reset_output()
# if statsResults:
#     statsResults = processResults(statsResults, nonMatchedWord)

# begin checking for triangulation of results

