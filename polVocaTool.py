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
    newPhraseCards = []

    for word in listOfPolishWords:
        if word[0] == '*':
            newPhraseCards.append(word[1:])
        else:
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
                    polishSourceWord = allDefs[0].get_text().capitalize()
                    print(f'Polish root word is: {polishSourceWord}')
                    firstEngDef = allDefs[1].find('a', class_="plainLink")
                    
                    try:
                        engDef = firstEngDef.get_text()
                        if 'ć' in engDef.lower():
                            print(f'Found Polish verb: {engDef}. Verb added to source word list')
                            listOfPolishWords.append(engDef)
                            continue
                        else:
                            print(f'Found definition: {engDef}')
                        try:
                            newAnkiCards.append(f'{polishSourceWord}:{engDef.capitalize()}')
                        except:
                            print('Failed to write to file.')

                    except:
                        print('Failed to extract text')


                except:
                    print('Definition not found. BS4 Parsing error?')
            
                    
            except:
                print(f'Error finding {word}: not in dictionary?')



    return newAnkiCards, newPhraseCards


### META FUNCTIONS

# makeNewPolAnkiCards - take words from .txt file, search for definitions, format results for anki and write.
def makeNewPolAnkiCards():
    newPolishWords = getPolishWords()
    cardFormattedPolWords, phraseCards = getDefinitionsForPolishWords(newPolishWords)
        
    resetPolishFile()

    vocaTools.writeUTFCardDump(cardFormattedPolWords, 'newPolishCards')
    if phraseCards:
        resetPolPhraseFile()
        vocaTools.writeUTFCardDump(phraseCards, 'newPolishPhrases')

#Retrieve words from dropbox file
getPolishWords =vocaTools.getWords(dropBoxPolFile)

#Reset anki file to prevent repeat cards
resetPolishFile = vocaTools.resetTextFile('newPolishCards')
resetPolPhraseFile = vocaTools.resetTextFile('newPolishPhrases')

#Perform main task - produce cards
makeNewPolAnkiCards()


