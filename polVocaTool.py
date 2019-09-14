import os, codecs, webbrowser
import requests as req
import bs4

os.chdir(r'C:\Users\User\.spyder-py3\KoreanVocaTool')
dropBoxKorFile = (r'C:\Users\User\Dropbox\New Words\koreanWords.txt')
dropBoxPolFile = (r'C:\Users\User\Dropbox\New Words\polishWords.txt')
headers = {'User-Agent' : 'Chrome/70.0.3538.77'}
korDictURL = r'https://krdict.korean.go.kr/eng/dicSearch/search?nation=eng&nationCode=6&ParaWordNo=&mainSearchWord='
polDictURL = r'https://www.diki.pl/slownik-angielskiego?q='


def getWords(FilePath):
    def getWordsFromTxt():
        with codecs.open(FilePath, 'r', 'utf-8') as textFile:
            contents = textFile.readlines()
            words = [word.strip() for word in contents]
        return words
    return getWordsFromTxt

getKoreanWords = getWords(dropBoxKorFile)

getPolishWords = getWords(dropBoxPolFile)




            
def getDefinitionsForKorWords(listOfKorWords):

    newAnkiCards = []
    for word in listOfKorWords:
        try:
            searchWord = word #Placeholder for testing, replace with function variable
            searchURL = korDictURL + searchWord

            res = req.get(searchURL, headers=headers)
            res.raise_for_status()

            soup = bs4.BeautifulSoup(res.text, features='lxml')

            resultWord = soup.find('li', id="article0") # NB: If this fails, it means the search failed.
            resultKorWord = soup.select('strong')[0]
            koreanWord = resultKorWord.get_text().strip()
            koreanWord = koreanWord[1:-1]


            definition = soup.select('p.defFont6')[0]
            englishDef = definition.get_text().strip()

            if '하다' in koreanWord:
                englishDef = f'to {englishDef}'

            ankiFormatWord = f'{koreanWord}:{englishDef}'

            newAnkiCards.append(ankiFormatWord)
        except:
            print(f'Error finding {word}: Not in dictionary?')

    return newAnkiCards


def getDefinitionsForPolishWords(listOfPolishWords):

    newAnkiCards = []
    for word in listOfPolishWords:
        try:
            searchWord = word #Placeholder for testing, replace with function variable
            searchURL = polDictURL + searchWord

            # webbrowser.open_new_tab(searchURL)

            res = req.get(searchURL, headers=headers)
            res.raise_for_status()

            soup = bs4.BeautifulSoup(res.text, features='lxml')

            # engDefs = soup.find('span', class_="hw")
            
            findFirstDefinition = soup.find('a', class_='plainLink')

            engDef = findFirstDefinition.get_text()
            
            newAnkiCards.append(f'{word}:{engDef}')
        except:
            print(f'Error finding {word}: not in dictionary?')



    return newAnkiCards


def resetTextFile(textFileToReset):
    def resetCardDumpFile():
        with open(rf'.\ankiText\{textFileToReset}.txt', 'w+') as ankiCardTextFile:
            ankiCardTextFile.write('')
        return
    return resetCardDumpFile

resetKoreanFile = resetTextFile('newKoreanCards')
resetPolishFile = resetTextFile('newPolishCards')


def writeUTFCardDump(cardsToWrite, textFileToWrite):
    with codecs.open(rf'.\ankiText\{textFileToWrite}.txt', 'a+', encoding='utf-8') as ankiCardTextFile:
        for card in cardsToWrite:
            print(f'Writing {card} to anki Text file...')
            ankiCardTextFile.write(card + '\n')
    print('All done!')


def makeNewKorAnkiCards():

    newKoreanWords = getKoreanWords()
    cardFormattedKorWords = getDefinitionsForKorWords(newKoreanWords)

    resetKoreanFile()

    writeUTFCardDump(cardFormattedKorWords, 'newKoreanCards')

def makeNewPolAnkiCards():
    newPolishWords = getPolishWords()
    cardFormattedPolWords = getDefinitionsForPolishWords(newPolishWords)
        
    resetPolishFile()

    writeUTFCardDump(cardFormattedPolWords, 'newPolishCards')

# makeNewKorAnkiCards()

makeNewPolAnkiCards()


