import nltk
import do_magic.voila as voila
import do_magic.dataQuery as sqlQuery
import do_magic.answerFinder as answer

def nerPersonTagging(question: str):
    find_persons = voila.structure_ne(voila.nltk_tagger(voila.process_text(question)))
    find_persons = [i[0] for i in find_persons]
    dict = {}
    if find_persons:
        for person in find_persons:
            dict[person] = [sqlQuery.search_stats_DB_noLike(person), sqlQuery.search_player_dB_noLike(person)]
            if checkifhit(dict): return False
            else: return  person, sqlQuery.search_stats_DB_noLike(person), sqlQuery.search_player_dB_noLike(person)
    if not find_persons: return False
    return dict

def checkifhit(dict: dict):
    for i in dict.values():
        if len(i[0]) == 0 and len(i[1]) == 0: return True

def removeName_fromQuery(personhit, question: str):
    for person in personhit.keys():
        if person.lower() in question: question = question.replace(person.lower(), '')
    x = question.find("\'s")
    if x: question = question.replace("\'s", '')
    return question

def attempt_one(question: str):
    tokenized = nltk.word_tokenize(question)
    tokenized = voila.get_stopwords(tokenized)
    if "\'s" in tokenized: tokenized.remove("\'s")
    if "s" in tokenized: tokenized.remove("s")
    j = 0
    stringg = ''
    for ss in tokenized:
        stringg = stringg + ss + " "
    dict = {}
    for i in range(j+1, len(tokenized)):
        x = "how tall is " + voila.singlequoteSQLfix(tokenized[j].capitalize()) + ' ' + voila.singlequoteSQLfix(
            tokenized[i].capitalize())
        y = voila.singlequoteSQLfix(tokenized[j].capitalize()) + ' ' + voila.singlequoteSQLfix(
            tokenized[i].capitalize())
        if 'shaq' in y.lower():
            ngram = n_gramplayerLookup('shaq')
            if ngram:
                name, stat, player = ngram
                dict[name] = [stat, player]
        else:
            NerTag = nerPersonTagging(x)
            if  NerTag:
                name, stat, player = NerTag
                if name and stat and player: dict[name] = [stat, player]
            else:
                ngram = n_gramplayerLookup(y)
                if ngram:
                    if y[len(y)-1 ] =="s": y = y[:len(y)-1]
                    name, stat, player = ngram
                    if name and stat and player:
                        y = nltk.word_tokenize(y.lower())
                        itemcount = 0
                        for item in y:
                            if item in name.lower():itemcount+=1
                        if itemcount == len(y):dict[name] = [stat, player]
        j += 1
    if dict: return dict
    else: return False

def n_gramplayerLookup(playernamewithlike):
    x  = sqlQuery.search_stats_DB(playernamewithlike)
    y= sqlQuery.search_player_dB(playernamewithlike)
    if x and y:
        name = y[0][0]
        return name,x,y
    else: namefound = throwname_atDB(playernamewithlike)
    if namefound:
        namefound = voila.singlequoteSQLfix(namefound)
        x = sqlQuery.search_stats_DB(namefound)
        y = sqlQuery.search_player_dB(namefound)
        if x and y:
            name = y[0][0]
            return name, x, y
    else: return False





def parseQuestion(question):
    personhit = attempt_one(question)
    if not personhit: personhit = throwname_atDB(question)
    elif not personhit: return getMinMax(question)
    else: question = removeName_fromQuery(personhit, question)
    tokenized = nltk.word_tokenize(question)

    minimumQualifiers = ["minimum", "min", "least", "lowest", "smallest", "shortest", "bottom","lesser", "less", "worst"]
    maximumQualifiers = ["maximum", "most", "max", "highest", "biggest", "tallest", "top", "heaviest", "higher", "better", "taller", "many", "more", "best"]
    tableName = "placeholder"
    min = False
    max = False
    who = False
    when = False
    year = False
    for word in tokenized:
        if "\'" in word:
            tokenized.remove(word)
        elif word == "when" or word == "year":
            when = True
        elif word == "who":
            who = True
        elif word.isnumeric():
            if 1949 < int(word) < 2019 or int(word) < 5: year = int(word)
            else: return "we do not have stats for that year"
        elif word.lower() in minimumQualifiers: min = True
        elif word.lower() in maximumQualifiers: max = True

    tokenized = voila.get_stopwords(tokenized)
    PRE_basewords = tokenized
    tokenized = voila.get_basewords(tokenized)
    if isinstance(personhit, dict):
        tablehit = get_searchTable_andName(tokenized)
        if not tablehit: tablehit = get_searchTable_andName(PRE_basewords)
        if not tablehit: return "unable to find match"
        else: tableInfo, tableName = tablehit
        if tableName == "player_data":
            return getPlayerData(personhit, tableInfo,min, max, year)
        elif tableName == "stats":
            return getStats(personhit, tableInfo, min, max, year, who, when)
    else:
        minmaxValuegeneral = getMinMax(tokenized, PRE_basewords,max, min, year)
        if minmaxValuegeneral: return minmaxValuegeneral
    return "unable to find match"


def raw_input_to_N_tuples(string, list_of_tuples):
    for row in list_of_tuples:
        if row[0] == string:
            return row


def get_searchTable_andName(tokenized):
    n_Gram = ''
    for word in tokenized:
        result = sqlQuery.search_phrase_DB(word)
        if result: n_Gram = n_Gram + word + ' '
    n_Gram = sqlQuery.search_EXACT_phrase(n_Gram.strip())
    if not n_Gram:
        return 0
    n_Gram = n_Gram[0]
    return n_Gram, n_Gram[5]

def stats_true(min, max, year, statsResults, wordResults, nonMatchedWord):
    # function 3
    if min:
        if year:
            voila.addToList(statsResults, sqlQuery.search_stats_min_DB(wordResults[3], year))
            return statsResults[0][0]
        else:
            voila.addToList(statsResults, sqlQuery.search_stats_min_no_year_DB(wordResults[3]))
            return statsResults[0][0]
    elif max:
        if year:
            voila.addToList(statsResults, sqlQuery.search_stats_max_DB(wordResults[3], year))
            return statsResults[0][0]
        else:
            voila.addToList(statsResults, sqlQuery.search_stats_max_no_year_DB(wordResults[3]))
            return statsResults[0][0]
    else:
        statsResults = answer.processResults(statsResults,
                                             nonMatchedWord)  # processResults begins triangulation.
    if year:
        statsResults = answer.find_with_year(year, statsResults)
    # elif max:
    #     search max of results #max of array
    # elif min:
    #     search min of results #min of array
    elif not isinstance(statsResults, tuple):
        statsResults = voila.get_most_recent(statsResults)
    if isinstance(statsResults, tuple):
        playerName = voila.singlequoteSQLfix(statsResults[0])
        index_for_answer = wordResults[4]
        return statsResults[index_for_answer]
    else:
        return statsResults
        # end function 3

def player_data_true(playerResults, nonMatchedWord):
    # function 2
    playerResults = answer.processResults(playerResults, nonMatchedWord)  # processResults begins triangulation.
    if isinstance(playerResults, tuple):
        playerName = voila.singlequoteSQLfix(playerResults[0])
    else:
        return playerResults
    # end function 2

def max_from_playerData_returnPerson(personhit:dict, tableInfo):
    val = {}
    for person, values in personhit.items():
        values = values[1]
        if not isinstance(values[0][tableInfo[4]], int):
            if values[0][tableInfo[4]].find('\'')!= -1: fix_value = values[0][tableInfo[4]].replace('\'', '')
            if fix_value.find(' ') != -1: fix_value = fix_value.replace(' ', '.')
            val[person] = float(fix_value)
        else: val[person] = float(values[0][tableInfo[4]])
    print(val)
    truemax = max(val, key=val.get)
    edge =  edgecase(val)
    return edge if edge else truemax

def min_from_playerData_returnPerson(personhit:dict, tableInfo):
    val = {}
    for person, values in personhit.items():
        values = values[1]
        if not isinstance(values[0][tableInfo[4]], int):
            if values[0][tableInfo[4]].find('\'') != -1: fix_value = values[0][tableInfo[4]].replace('\'', '')
            if fix_value.find(' ') != -1: fix_value = fix_value.replace(' ', '.')
            val[person] = float(fix_value)
        else:
            val[person] = float(values[0][tableInfo[4]])
    print(val)
    truemax = min(val, key=val.get)
    edge = edgecase(val)
    return edge if edge else truemax

def edgecase(val):
    l = [v for v in val.values()]
    return "they are the same" if len(set(l)) == 1 else False

def getPlayerData(personhit: dict, tableInfo,min, max, year):
    if min and year: pass
    elif min and not year: return min_from_playerData_returnPerson(personhit, tableInfo)
    elif max and year: pass
    elif max and not year: return max_from_playerData_returnPerson(personhit, tableInfo)
    elif year and not max and not min: pass
    elif not year and not max and not min:
        for person in personhit.values():
            person = person[1]
            return person[0][tableInfo[4]]

def getMin_from_N_ppl_noDate_returnName(personhit, tableInfo):
    getmin = {}
    for person, personstats in personhit.items():
        personstats = personstats[0]
        getmin[person] = float(minFrom_one_player_return_name(personstats, tableInfo))
        print(f'name: {person}: min: {minFrom_one_player_return_name(personstats, tableInfo)}')
    return min(getmin, key=getmin.get)

def getstat_by_Year_returnStat(personhit, tableInfo, year):
    for person in personhit.values():
        person = person[0]
        for j in range(len(person)):
            if person[j][2] != "Unknown":
                if year == person[j][2]: return person[j][tableInfo[4]]


def getMax_from_N_ppl_noDate_returnName(personhit, tableInfo):
    getmax = {}
    for person, personstats in personhit.items():
        personstats = personstats[0]
        getmax[person] = float(maxFrom_one_player_return_name(personstats, tableInfo))
        if maxFrom_one_player_return_name(personstats, tableInfo) < 1:
            print(f'name: {person}: max: Unknown')
        else:
            print(f'name: {person}: max: {maxFrom_one_player_return_name(personstats, tableInfo)}')
    return max(getmax, key=getmax.get)

def get_max_onePerson_return_date(personhit: dict, tableInfo):
    highest = [0.0, ""]
    for person in personhit.values():
        person = person[0]
        for i in range(len(person)):
            if person[i][tableInfo[4]] != "Unknown":
                if float(person[i][tableInfo[4]]) > float(highest[0]):
                    highest[0] = float(person[i][tableInfo[4]])
                    highest[1] = i
    return person[highest[1]][2]

def get_min_onePerson_return_date(personhit: dict, tableInfo):
    highest = [999999.0, ""]
    for person in personhit.values():
        person = person[0]
        for i in range(len(person)):
            if person[i][tableInfo[4]] != "Unknown":
                if float(person[i][tableInfo[4]]) < float(highest[0]):
                    highest[0] = float(person[i][tableInfo[4]])
                    highest[1] = i
    return person[highest[1]][2]

def getMin_withYear_andName_returnName(personhit: dict, tableInfo: list, year):
    get_name = {}
    for x,person in personhit.items():
        person = person[0]
        for j in range(len(person)):
            if person[j][2] != "Unknown":
                if year == person[j][2]:
                    get_name[x] =  float(person[j][tableInfo[4]])
    return min(get_name, key=get_name.get)

def getMax_withYear_andName_returnName(personhit, tableInfo, year):
    get_name = {}
    for x, person in personhit.items():
        person = person[0]
        for j in range(len(person)):
            if person[j][2] != "Unknown":
                if year == person[j][2]:
                    get_name[x] = float(person[j][tableInfo[4]])
    return max(get_name, key=get_name.get)

def getStats(personhit: dict, tableInfo: list, minr, maxr, year, who, when):
    if when and maxr:
        return get_max_onePerson_return_date(personhit, tableInfo)
    elif when and minr:
        return get_min_onePerson_return_date(personhit, tableInfo)
    elif minr and year and who:
        return getMin_withYear_andName_returnName(personhit, tableInfo, year)
    elif minr and not year and who:
        return getMin_from_N_ppl_noDate_returnName(personhit, tableInfo)
    elif maxr and year and who:
        return getMax_withYear_andName_returnName(personhit, tableInfo, year)
    elif maxr and not year and who:
        return getMax_from_N_ppl_noDate_returnName(personhit, tableInfo)
    elif year and not maxr and not minr:
       return getstat_by_Year_returnStat(personhit, tableInfo, year)
    elif not year and not maxr and not minr:
        for person in personhit.values(): return person[0][len(person[0])-1][tableInfo[4]]
    elif maxr and year:
        return getstat_by_Year_returnStat(personhit, tableInfo, year)
    elif minr:
        return getMin_stat_noYear_returnstat(personhit, tableInfo)
    elif maxr:
        return getMax_stat_noYear_returnstat(personhit, tableInfo)

def getMin_stat_noYear_returnstat(personhit, tableInfo):
    highest = [999999.0, ""]
    for person in personhit.values():
        person = person[0]
        for i in range(len(person)):
            if person[i][tableInfo[4]] != "Unknown":
                if float(person[i][tableInfo[4]]) < float(highest[0]):
                    highest[0] = float(person[i][tableInfo[4]])
                    highest[1] = i
    return person[highest[1]][tableInfo[4]]

def getMax_stat_noYear_returnstat(personhit, tableInfo):
    highest = [0.0, ""]
    for person in personhit.values():
        person = person[0]
        for i in range(len(person)):
            if person[i][tableInfo[4]] != "Unknown":
                if float(person[i][tableInfo[4]]) > float(highest[0]):
                    highest[0] = float(person[i][tableInfo[4]])
                    highest[1] = i
    return person[highest[1]][tableInfo[4]]

def minFrom_one_player_return_name(person: dict, tableInfo):
    highest = [999999.0, ""]
    for i in range(len(person)):
        if person[i][tableInfo[4]] != "Unknown":
            if float(person[i][tableInfo[4]]) < float(highest[0]):
                highest[0] = float(person[i][tableInfo[4]])
                highest[1] = i
    return highest[0]


def maxFrom_one_player_return_name(person: dict, tableInfo):
    highest = [0.0, ""]
    for i in range(len(person)):
        if person[i][tableInfo[4]] != "Unknown":
            if float(person[i][tableInfo[4]]) > float(highest[0]):
                highest[0] = float(person[i][tableInfo[4]])
                highest[1] = i
    return highest[0]


def throw_atDB(tokenized: list, wordResults, playerResults,statsResults, nonMatchedWord):
    n_Gram = ''
    for word in tokenized:
        result = sqlQuery.search_phrase_DB(word)
        if result:
            voila.addToList(wordResults, result)
            n_Gram = n_Gram + word + ' '
        else:
            result = sqlQuery.search_player_dB(word)
            result_stat = sqlQuery.search_stats_DB(word)
            if result: voila.addToList(playerResults, result)
            if result_stat:
                voila.addToList(statsResults, result_stat)
            else:
                nonMatchedWord.append(word)
    return n_Gram.strip()

def throwname_atDB(question):
    if question[len(question)-1] == 's': question = question[:len(question)-1]
    tokenized = nltk.word_tokenize(question)
    tokenized = voila.get_stopwords(tokenized)
    tokenized = voila.get_basewords(tokenized)
    name = []
    listt = [set() for i in range(2)]
    i = 0
    for word in tokenized:
        if word[len(word) -1] == "s": word = word[:len(word)-1]
        result = sqlQuery.search_stats_DB(word)
        if result:
            for size in range(len(result)):
                name.append(result[size][0])
            listt[i] = set(name)
            name = []
            i+=1
    if listt[0] and not listt[1]:
        return listt[0].pop()
    if listt[0].intersection(listt[1]):
        namehit = listt[0].intersection(listt[1])
        namehit = namehit.pop()
        return namehit

    return False

def getMinMax(tokenized, PRE_basewords, maxx, minn, year):
    tablehit = get_searchTable_andName(tokenized)
    if not tablehit: tablehit = get_searchTable_andName(PRE_basewords)
    if tablehit: tableInfo, tableName = tablehit
    if year: year = str(year)

    if maxx and year:
        val = sqlQuery.search_stats_max_DB(tableInfo[3], year)
        return val[0][0] if val else False
    elif minn and year:
        val =  sqlQuery.search_stats_min_DB(tableInfo[3], year)
        return val[0][0] if val else False
    elif minn:
        val =  sqlQuery.search_stats_min_no_year_DB(tableInfo[3])
        return val[0][0] if val else False
    elif maxx:
        val =  sqlQuery.search_stats_max_no_year_DB(tableInfo[3])
        return val[0][0] if val else False
    else: return False