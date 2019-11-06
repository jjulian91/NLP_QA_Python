import nltk
from nltk.corpus import stopwords
import do_magic.voila as voila
import do_magic.questionParser as parse

def main():
    while 1:
        print("\tThis Database contains historical player data.  Some information is unavailable due to the changes\n"
              "\tin the statistics kept year over year.  This system will not return general team information such as\n "
              "\t\"who won the NBA finals?\".  ")
        value = input('Enter in a question: ')
        result = parse.parseQuestion(value)
        print(result)
        #print(f'RESULTS: {result}') if len(result) >= 1 else print('There are no results that match this question')
        voila.runstat()


if __name__ == '__main__':
    main()
