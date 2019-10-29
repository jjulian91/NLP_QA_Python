import nltk
import do_magic.voila as voila
import do_magic.dataQuery as sqlQuery
import do_magic.answerFinder as answer


#return from this statement " ("select * from phrase join lookup_table as LU on phrase.FK=LU.PK where Phrase like "
#              + "'%" + word + "%'") "
# is : [('tall', 56, 56, 'height', 5, 'player_data')]
# 0 = reference 1 = FK 2 = PK 3 = name of column 4 = column number (for getting answer). 5 is table where lookup is found
# also for building SQL statement when getting answer.
# todo we will need to start brain storming all use cases for what is expected as output.  We need to trap any "years"
#  used in the query and a few special words that we will have to update the DB for in the look up table.
#   we should meet early on wednesday 10/30 to start working on a better flow control for the program.
#    there is a new DB also in the folder please upload.


def parseQuestion(question):
    tokenized = nltk.word_tokenize(question)
    tagged_sentence = voila.tag_Sentence(tokenized)
    tagged_sentence = apostrophefix(tagged_sentence)
    nouns = []
    matches = []
    nonMatched = []
    allResults = []
    phrases = []
    category = "unknown"

    for word in tagged_sentence:
        if word[1] == "NNP" or word[1] == "NN":
            nouns.append(word[0])
            #print('this is a noun:' + word[0])
            category = "Person"
        else:
            nonMatched.append(word[0])

    for noun in nouns:
        result = sqlQuery.dbQuery("select * from player_data where name like " + "'%" + noun + "%'")
        allResults.append(result)
        if result:
            matches.append(result)
        else:
            nonMatched.append(noun)

    # use nonMatched to retrieve nouns that aren't matched to a name value.
    # search non matched with lookup table as well as the tagged sentences
    #for entry in allResults:
        #print(f'entry: \n{entry}')
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
                refined_word = singlequoteSQLfix(refined_word)

        if refined_word:
            result = sqlQuery.dbQuery("select * from player_data where name like " + "'%" + refined_word + "%'")
            if result:
                #print(f'there was a hit with {refined_word} after spellcheck')
                matches.append(result)

        #todo
        # this is good work --- we need to take the results from the phrase_matches and triangulate as we did in first
        # query.  From there we are going to be using the results from all the searches to find the actual answers
        # from the table and work on displaying them as the expected by user.  We should also reorganize the code.
        # search non nouns first.  -- take the result then search that table (ordinal index 5 from the sql statement I
        # created below) then do noun search on that table similar to the one I have below as well.  Then if no hits we
        # apply the same logic from previously where we capture all non matches and spell check then requery. (ONLY IF
        # ANSWER IS NOT FOUND IN FIRST 2 STATMENTS).
        #

        # if all else fails to search
        phrase_result = sqlQuery.dbQuery("select * from phrase join lookup_table as LU on phrase.FK=LU.PK where Phrase like "
              + "'%" + word + "%'")

        phrase_matches =[]
        # not sure which array to append too?? so just made one -___-

        if phrase_result:
            phrase_matches.append(phrase_result)
            #print(
            #    f'there was a hit in the \'[phrase]\' table with the word [{word}] having a result: \n{phrase_result}')

        #todo this is an issue --  we gotta get a better way to flatten ANY array to a single array.
        name = answer.find(allResults)
        #print("this is the print statment you need")
        flattened_phrase = answer.flatten(phrase_result)
        #print(flattened_phrase[5])
        #print(name)
        Qanswer = answer.flatten(sqlQuery.dbQuery("select * from "+ flattened_phrase[5] + " where name ="+ "'" + name[0] + "'"))
        info = Qanswer[flattened_phrase[4]]

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
    return info


# checks if theres an apostrophe e.g. D'angelo. Adds apostrophe for escape character in SQL --> d''angelo. if there is NO apostrophe then returns word
def singlequoteSQLfix(val):
    index = val.find("'")
    return val[:index] + "''" + val[index + 1:] if index != -1 else val


# modifies the query values to make them sql safe search.. eg: d'angelo 3's
def apostrophefix(words):
    for i, word in enumerate(words):
        if i >= len(words) - 1:
            break
        j = i + 1
        # case where three's splits into [three] & ['s], we make it one word [three's] and add the apostrophe to it -> [three''s] for sql safe search. then we remove the tuple ('s, POS) and return ("three''s", "null")
        if words[j][1] == "POS" and words[i][1] == "NN" or words[j][1] == "POS" and words[i][1] == "CD":
            concat = words[i][0] + words[j][0]
            concat = singlequoteSQLfix(concat)
            words[i] = (concat, "null")
            words.remove(words[j])
        else:
            # if the above is not the case e.g d'angelo. just fix it --> d''angelo and return it along with its part of speech
            words[i] = (singlequoteSQLfix(words[i][0]), words[i][1])
    # case where o'neal is last in the query --> o''neal
    # if last value -> [three''s] already has been modified then skip. but for cases where o'neal is last . make it o''neal
    if words[len(words) - 1][0].find("''") == -1:
        words[len(words) - 1] = singlequoteSQLfix(words[len(words) - 1][0]), words[len(words) - 1][1]
    return words
