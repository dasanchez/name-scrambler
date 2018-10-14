"""
voldemot_utils
Helper functions for voldemot package
"""
def loadDictionary(filename):
    """ reads words line by line from a file and returns them in a list """
    # wordList = []
    wordFile = open(filename, "r")
    wordList = [word.rstrip().lower() for word in wordFile if "'" not in word]
    wordFile.close()
    # print("Read " + str(len(wordList)) + " words.")
    return wordList

def wordIsPresent(word, soup):
    """ checks if the word can be assembled with the characters in the soup """
    testWord = word
    for letter in soup:
        testWord = testWord.replace(letter, "", 1)
    return not testWord

def getWordList(wordsFileName, letters):
    """
    Fills wordsFound list with words found in the letters string.
    wordfound is a dictionary with a word as a key and the length as a value
    """
    wordsFound = []
    # Load dictionary
    wordList = loadDictionary(wordsFileName)

    # Check if a word can be assembled from the letters available.
    # If so, add it to the wordsFound list.
    for word in wordList:
        if wordIsPresent(word, letters):
            wordsFound.append(word)

    return wordsFound

def getWordsEqualTo(wordList, targetLength):
    """ return list of words of a specified length in the list """
    return [word for word in wordList if len(word) == targetLength]

def getWordsUnder(wordList, targetLength):
    """ return list of words of a specified length in the list """
    return [word for word in wordList if len(word) < targetLength]

async def findWordCombinations(wordsFound, letters, wordCount):
    ''' find 2+ word combinations '''
    fullMatch = []
    rootList = getWordsUnder(wordsFound, len(letters) - (wordCount - 2))
    tempWords = rootList.copy()
    lettersLength = len(letters)

    for root in rootList:
        # traverse the remainder of the list until it's all gone
        baggageCounter = 1
        prefixList = [root]
        for baggageCounter in range(2, wordCount+1):
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
            prefixList = newPrefixList.copy()

        tempWords.remove(root)

    return fullMatch
