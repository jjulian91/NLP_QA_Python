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
    persons = []
    category = "unknown"
    for word in tagged_sentence:
        print(f'word: {word}')
        if word[1] == "NN":
            nouns.append(word[0])
            print('this is a noun:' + word[0])
            category = "Noun"

        if word[1] == "NNP":
            persons.append(word[0])
            category = "Person"
            print('this is a persons name:' + word[0])
        else:
            nonMatched.append(word[0])

    for person in persons:
        print("select * from player_data where name == " + "'" + person + "'")
        result = sqlQuery.dbQuery("select * from player_data where name like " + "'%" + person + "%'")
        if result:
            matches.append(result)
        else:
            # nonMatched.append(person)
            print('That person is not in our database.')

    # for noun in nouns:
    #     print("select * from player_data where noun == " + "'" + person + "'")
    #     result = sqlQuery.dbQuery("select * from player_data where name like " + "'%" + noun + "%'")
    #     if result:
    #         matches.append(result)
    #     else:
    #         nonMatched.append(person)
    # use nonMatched to retrieve nouns that aren't matched to a name value.
    # search non matched with lookup table as well as the tagged sentences

    nonMatched = voila.get_stopwords(nonMatched)
    for word in nonMatched:
        print(word)
        print(sqlQuery.dbQuery("select * from phrase where Phrase like " + "'%" + word + "%'"))

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
