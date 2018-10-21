"""
voldemot_utils
Helper functions for voldemot package
"""
import asyncio

def readDictionary(filename):
    """ reads words line by line from a file and returns them in a list """
    wordFile = open(filename, "r")
    wordList = [word.rstrip().lower() for word in wordFile if "'" not in word]
    wordFile.close()
    return wordList

def wordIsPresent(word, soup):
    """ checks if the word can be assembled with the characters in the soup """
    for letter in soup:
        word = word.replace(letter, "", 1)
    return not word

def getWordList(dictFileName, letters):
    """ returns a list with words found in the letters string using the dictionary in the filename """
    return [word for word in readDictionary(dictFileName) if wordIsPresent(word, letters)]

def getWordsEqualTo(wordList, targetLength):
    """ return list of words of a specified length in the list """
    return [word for word in wordList if len(word) == targetLength]

def getWordsUnder(wordList, targetLength):
    """ return list of words of a specified length in the list """
    return [word for word in wordList if len(word) < targetLength]

def printProgressBar(iteration, total, suffix='',
                     decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    Credit: @greenstick
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    progressBar = fill * filledLength + '-' * (length - filledLength)
    print(f" |{progressBar}| {percent}% {suffix}", end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()

async def findWordCombinations(wordsFound, letters, wordCount, pauseInterval = 10000, pauseLength = 0.05, verbose = False):
    ''' find 2+ word combinations '''
    fullMatch = []
    rootList = getWordsUnder(wordsFound, len(letters) - (wordCount - 2))
    tempWords = rootList.copy()
    lettersLength = len(letters)
    pauseCount = pauseInterval
    total = 0
    percent = 0

    for root in rootList:
        # traverse the remainder of the list until it's all gone
        prefixList = [root]
        for baggageCounter in range(2, wordCount + 1):
            newPrefixList = []
            for prefix in prefixList:
                lastPrefix = prefix.split(' ')[-1]
                tempList = tempWords[tempWords.index(lastPrefix):]
                collapsedPrefix = prefix.replace(" ", "")
                spotsAvailable = lettersLength - len(collapsedPrefix)

                if baggageCounter == wordCount:
                    for tempWord in getWordsEqualTo(tempList, spotsAvailable):
                        if sorted(collapsedPrefix + tempWord) == sorted(letters):
                            fullMatch.append(f"{prefix} {tempWord}")
                else:
                    baggageLeft = spotsAvailable - (wordCount - baggageCounter - 1)
                    for tempWord in getWordsUnder(tempList, baggageLeft):
                        if wordIsPresent(collapsedPrefix + tempWord, letters):
                            newPrefixList.append(f"{prefix} {tempWord}")

                pauseCount -= 1

                if pauseCount == 0:
                    pauseCount = pauseInterval
                    await asyncio.sleep(pauseLength)
                    
            prefixList = newPrefixList.copy()

        tempWords.remove(root)
        
        if verbose:
            total += 1
            newPercent = int(total * 100 / len(rootList))
            if newPercent != percent:
                percent = newPercent
                printProgressBar(total, len(rootList), length=50)
        
    return fullMatch
