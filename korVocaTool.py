import os, codecs, webbrowser
import requests as req
import bs4
import vocaTools

os.chdir(r'C:\Users\User\.spyder-py3\vocaSearchTool')
dropBoxKorFile = (r'C:\Users\User\Dropbox\New Words\koreanWords.txt')
headers = {'User-Agent' : 'Chrome/70.0.3538.77'}
korDictURL = r'https://endic.naver.com/search.nhn?sLn=en&searchOption=all&query='



# getDefinitionsForKorWords - with list of string Kor. words, retrieve definition from dict via BS4.             
def getDefinitionsForKorWords(listOfKorWords):

    newAnkiCards = []
    newPhrasecards = []
    for word in listOfKorWords:
        if word[0] == '*':
            newPhrasecards.append(word[1:])
        else:
            try:
                searchWord = word #Placeholder for testing, replace with function variable
                searchURL = korDictURL + searchWord
                

                res = req.get(searchURL, headers=headers)
                res.raise_for_status()

                soup = bs4.BeautifulSoup(res.text, features='lxml')

                try:    
                    resultWord = soup.find('span', class_="fnt_k05") # NB: If this fails, it means the search failed.

                    
                except:
                    print(f"Error finding {word}: BS4 failed to find CSS selector 'span class=fnt_k05'")
                    


                try:
                    textOnlyWord = resultWord.get_text().strip()
                    print(f'Found "{word}", with definition {textOnlyWord}.')
                except:
                    print('Error extracting text from tag')
                    

                
                koreanWord, englishDef = vocaTools.handleKorVerbs(word, textOnlyWord)

                ankiFormatWord = f'{koreanWord}:{englishDef}'

                newAnkiCards.append(ankiFormatWord)

            except:
                print(f'Error finding {word}: Not in dictionary?')

    return newAnkiCards, newPhrasecards


### META FUNCTIONS

# makeNewKorAnkiCards - take words from .txt file, search for definitions, format results for anki and write.
def makeNewKorAnkiCards():

    newKoreanWords = getKoreanWords()
    cardFormattedKorWords, phraseCards = getDefinitionsForKorWords(newKoreanWords)

    resetKoreanFile()

    vocaTools.writeUTFCardDump(cardFormattedKorWords, 'newKoreanCards')
    if phraseCards:
        resetKoreanPhraseFile()
        vocaTools.writeUTFCardDump(phraseCards, 'newKoreanPhrases')

#Retrieve words from dropbox file
getKoreanWords = vocaTools.getWords(dropBoxKorFile)

#Reset anki file to prevent repeat cards
resetKoreanFile = vocaTools.resetTextFile('newKoreanCards')
resetKoreanPhraseFile = vocaTools.resetTextFile('newKoreanPhrases')

#Perform main task - produce cards
makeNewKorAnkiCards()


