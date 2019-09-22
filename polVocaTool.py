import os, codecs, webbrowser
import requests as req
import bs4
import vocaTools

os.chdir(r'C:\Users\User\.spyder-py3\vocaSearchTool')
dropBoxPolFile = (r'C:\Users\User\Dropbox\New Words\polishWords.txt')
headers = {'User-Agent' : 'Chrome/70.0.3538.77'}
polDictURL = r'https://www.diki.pl/slownik-angielskiego?q='


# getDefinitionsForPolishWords - with list of string Pol. words, retrieve definitions from dict via BS4
def getDefinitionsForPolishWords(listOfPolishWords):

    newAnkiCards = []

    for word in listOfPolishWords:
        try:
            print(f'Searching for word {word}...')
            searchWord = word #Placeholder for testing, replace with function variable
            searchURL = polDictURL + searchWord

            # webbrowser.open_new_tab(searchURL)

            res = req.get(searchURL, headers=headers)
            res.raise_for_status()

            soup = bs4.BeautifulSoup(res.text, features='lxml')
            try:
                allDefs = soup.findAll('span', class_="hw")
            except:
                print('Error 1: BS4 Parsing failed at first search')

            try:
                firstEngDef = allDefs[1].find('a', class_="plainLink")
                print(f'Definition found: {firstEngDef}')

                try:
                    engDef = firstEngDef.get_text()

                    try:
                        newAnkiCards.append(f'{word.capitalize()}:{engDef.capitalize()}')
                    except:
                        print('Failed to write to file.')

                except:
                    print('Failed to extract text')


            except:
                print('Definition not found. BS4 Parsing error?')
        
                
        except:
            print(f'Error finding {word}: not in dictionary?')



    return newAnkiCards

### META FUNCTIONS

# makeNewPolAnkiCards - take words from .txt file, search for definitions, format results for anki and write.
def makeNewPolAnkiCards():
    newPolishWords = getPolishWords()
    cardFormattedPolWords = getDefinitionsForPolishWords(newPolishWords)
        
    resetPolishFile()

    vocaTools.writeUTFCardDump(cardFormattedPolWords, 'newPolishCards')

#Retrieve words from dropbox file
getPolishWords =vocaTools.getWords(dropBoxPolFile)

#Reset anki file to prevent repeat cards
resetPolishFile = vocaTools.resetTextFile('newPolishCards')

#Perform main task - produce cards
makeNewPolAnkiCards()


