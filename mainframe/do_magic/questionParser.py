import nltk
import do_magic.voila as voila
import do_magic.dataQuery as sqlQuery
import do_magic.answerFinder as answer


def parseQuestion(question):
    tokenized = nltk.word_tokenize(question)
    tagged_sentence = voila.tag_Sentence(tokenized)
    nouns = []
    matches = []
    nonMatched = []
    allResults = []
    category = "unknown"
    for word in tagged_sentence:
        if (word[1] == "NNP" or word[1] == "NN"):
            nouns.append(word[0])
            print('this is a noun:' + word[0])
            category = "Person"
        else:
            nonMatched.append(word[0])

    for noun in nouns:
        # "select * from player_data where name == " + "'" + noun + "'"
        result = sqlQuery.dbQuery("select * from player_data where name like " + "'%" + noun + "%'")
        allResults.append(result)
        if result != []:
            matches.append(result)
        else:
            nonMatched.append(noun)

    # use nonMatched to retrieve nouns that aren't matched to a name value.
    # search non matched with lookup table as well as the tagged sentences
    for entry in allResults:
        print(entry)
    nonMatched = voila.get_stopwords(nonMatched)
    for word in nonMatched:
        print(f'nonmatched words:   {word}')
        refined_word = voila.spell_check(word)
        if refined_word:
            result = sqlQuery.dbQuery("select * from player_data where name like " + "'%" + refined_word + "%'")
            if result:
                print(f'there was a hit with {refined_word} after spellcheck')
                matches.append(result)
                # answer.find(matches)
        else:
            print(f'[{word}] is either correctly spelled and not in our DB or it could not be spellchecked')
        # put spellcheck on nonmatched words
        # run same sql from noun
        # if hit pass to all result
        # run answere.finder on all results/
        sqlQuery.dbQuery("select * from phrase where Phrase like " + "'%" + word + "%'")

    # begin chceking for row matching in query.
    # for words in tagged_sentence:
    #     if (category == "Person") :
    #         select_statement = "select * from player_data where name like '%" + words[0] + "%'"
    #     elif (category == "unknown" or category == "Location") and (words[1] == 'WP' or words[1] == "WP$"):
    #         category = "Name"
    #         select_statement = "select * from player_data where name like '%" + words[0] + "%'"
    #     elif (category == "unknown") and (words[1] == "WRB" or words[1] == "WDT"):
    #         category = "Location"
    #     else:
    #         category = "unknown"
    # # this is a beginning to the select statements -- we will need to build upon this and pass it to the
    # dataQuery class.  Then we will be able to return entire rows and parse them from the main file.
    # entries = sqlQuery.dbQuery(select_statement)
    return answer.find(matches)
