import codecs

def getWords(FilePath):
    def getWordsFromTxt():
        with codecs.open(FilePath, 'r', 'utf-8') as textFile:
            contents = textFile.readlines()
            words = [word.strip() for word in contents]
        return words
    return getWordsFromTxt


def resetTextFile(textFileToReset):
    def resetCardDumpFile():
        with open(rf'.\ankiText\{textFileToReset}.txt', 'w+') as ankiCardTextFile:
            ankiCardTextFile.write('')
        return
    return resetCardDumpFile

def writeUTFCardDump(cardsToWrite, textFileToWrite):
    with codecs.open(rf'.\ankiText\{textFileToWrite}.txt', 'a+', encoding='utf-8') as ankiCardTextFile:
        for card in cardsToWrite:
            print(f'Writing {card} to anki Text file...')
            ankiCardTextFile.write(card + '\n')
    print('All done!')


def handleKorVerbs(inVerb, inEng):
    if '다' in inVerb[-1:]:
        if 'to' not in inEng[0:3].strip().lower():
            return (inVerb, 'To ' + inEng)
    else:
        return (inVerb, inEng.capitalize())



