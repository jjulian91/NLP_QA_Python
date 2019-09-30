import nltk
from nltk.corpus import stopwords
import do_magic.voila as voila
import do_magic.dataQuery as sqlQuery

def main():
    while(1):
        category = "blank"
        value = input('Enter in a question: ')
        tagged_sentence = voila.word_Magic(value)
        print(tagged_sentence)
        for words in tagged_sentence:
            if words[1] == "NNP" or words[1] == "NNPS":
                category = "Name"
            elif words[1] == 'WP' or words[1] == "WP$":
                category = "Person"
            elif words[1] == "WRB" or words[1] == "WDT":
                category = "Location"
        print(category)
        voila.runstat()
        sqlQuery.dbQuery(category)

if __name__ == '__main__':
    main()
