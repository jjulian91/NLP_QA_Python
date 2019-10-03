import do_magic.voila as voila
import do_magic.dataQuery as sqlQuery
import do_magic.answerFinder as answer
def parseQuestion(question):
    tagged_sentence = voila.word_Magic(question)
    print(tagged_sentence)
    category = "unknown"
    select_statement = "select * from player_data"
    for words in tagged_sentence:
        if (category == "unknown" or category == "Name" or category == "Location") \
                and (words[1] == "NNP" or words[1] == "NNPS" or words[1] == "NNS" or words[1] == "NN"):
            category = "Person"
            select_statement = "select * from player_data where name like '%" + words[0] + "%'"
        elif (category == "unknown" or category == "Location")\
                and (words[1] == 'WP' or words[1] == "WP$"):
            category = "Name"
            select_statement = "select * from player_data where name like '%" + words[0] + "%'"
        elif (category == "unknown") and (words[1] == "WRB" or words[1] == "WDT"):
            category = "Location"
        else:
            category = "unknown"
    # this is a beginning to the select statements -- we will need to build upon this and pass it to the
    # dataQuery class.  Then we will be able to return entire rows and parse them from the main file.
    print(select_statement)
    entries = sqlQuery.dbQuery(select_statement)
    return answer.find(category, entries)

