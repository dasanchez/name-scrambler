"""
voldemot

Takes a set of letters (such as a name) and assembles combinations of words based on it.
Using English word list from SCOWL.
The results are output to a text file: [input]-iter.txt

Usage:
python voldemot letters [filename] [slots]

For example,
python voldemot.py albertcamus words/voldemot-dict.txt 2

will yield a text file called albert-camus.iter with 1125
combinations, "a clubmaster" and "cabal muster" to
"macabre slut" and "tsamba ulcer".
"""

import sys
import re
import time
from collections import Counter
import asyncio
import voldemot_utils as vol
import wordDB

def main(args):
    """ main program """
    start = time.time()

    worddb = wordDB.wordDB()
    worddb.query("CREATE TABLE words(word text, length int)")

    # for i in enumerate(args):
        # print(i)

    if len(args) < 2:
        print("Not enough arguments.\nUsage:\npython name-scrambler letters [filename]")

    # load source soup
    letters = args[1]

    # remove spaces and non-alphabetical characters
    letters = re.sub(r"\W?\d?", "", letters).lower()
    sortedLetters = sorted(list(letters))

    print("Source soup (" + letters + ") has " + str(len(letters)) + " characters")

    # generate dictionary file name
    wordFileName = "words/voldemot-dict.txt"
    if len(args) > 3:
        wordFileName = args[2]

    # set number of slots
    wordCount = 3
    if len(args) > 3:
        wordCount = int(args[3])

    # find words present in the soup
    wordsFound = vol.findWords(wordFileName, letters, worddb)
    print("Found " + str(len(wordsFound)) + " words.")

    print(sorted(wordsFound, key=len))

    wordDict = { word: len(word) for word in wordsFound }

    fullMatch = []

    print("1-word matches:")
    for word in getWordsOfLength(wordDict, len(letters)):
        if sorted(letters) == sorted(word):
            fullMatch.append(word)

    print("2-word matches:")
    wordList = wordsFound.copy()
    for word in wordsFound:
        wordList.remove(word)
        for second in getWords(wordList, len(letters) - len(word)):
            testCombo = word + second
            if sorted(testCombo) == sorted(letters):
                fullMatch.append(word + ' ' + second)

    print("3-word matches:")
    wordList = wordsFound.copy()
    for word in wordsFound:
        wordList.remove(word)
        secondList = wordList.copy()
        for second in getWordsUnder(wordList, len(letters) - len(word)):
            secondList.remove(second)
            twoWordCombo = word + second
            thirdList = secondList.copy()
            for third in getWordsEqual(thirdList, len(letters) - len(twoWordCombo) ):
                thirdList.remove(third)
                testCombo = twoWordCombo + third
                if sorted(testCombo) == sorted(letters):
                    fullMatch.append(word + ' ' + second + ' ' + third)

    # print("4-word matches:")
    # wordList = wordsFound.copy()
    # for word in wordsFound:
    #     wordList.remove(word)
    #     secondList = wordList.copy()
    #     for second in getWordsUnder(wordList, len(letters) - len(word)):
    #         secondList.remove(second)
    #         twoWordCombo = word + second
    #         thirdList = secondList.copy()
    #         for third in getWordsUnder(thirdList, len(letters) - len(twoWordCombo) ):
    #             thirdList.remove(third)
    #             testCombo = twoWordCombo + third
    #             if sorted(testCombo) == sorted(letters):
    #                 # print(word + ' ' + second + ' ' + third)
    #                 fullMatch.append(word + ' ' + second + ' ' + third)


    # generate all possible and put them in the fullMatch list
    # loop = asyncio.get_event_loop()
    # fullMatch = loop.run_until_complete(generateList(sortedLetters, wordCount, worddb))
    # loop.close()

    print("There are " + str(len(fullMatch)) + " full matches.")

    # for entry in fullMatch:
    #     myStr = ""
    #     for word in entry:
    #         myStr = myStr + word + " "
    #     print(myStr)

    end = time.time()
    print(str(int(end-start)) + " seconds elapsed")

def getWordsEqual(wordList, targetLength):
    """ return list of words of a specified length in the list """
    return [ word for word in wordList if len(word) == targetLength ]

def getWordsUnder(wordList, targetLength):
    """ return list of words of a specified length in the list """
    return [ word for word in wordList if len(word) < targetLength ]

def getWords(wordList, targetLength):
    """ return list of words of a specified length in the list """
    return [ word for word in wordList if len(word) <= targetLength ]

def getWordsOfLength(wordDict, targetLength):
    """ return list of words of a specified length in the dictionary """
    return [ word for word, wordLen in wordDict.items() if wordLen == targetLength ]

def voldemot(letters, wordsRequested):
    """ simplified function call that always goes to the standard dictionary """
    worddb = wordDB.wordDB()
    worddb.query("CREATE TABLE words(word text, length int)")

    # remove spaces and non-alphabetical characters
    letters = re.sub(r"\W?\d?", "", letters).lower()
    letters = letters[:16]

    vol.findWords("words/voldemot-dict.txt", letters, worddb)
    fullMatch = generateList(sorted(letters), wordsRequested, worddb)
    return letters, fullMatch

async def generateList(sortedSoup, wordCount, worddb):
    """ Returns a list of valid combinations in fullMatch """
    fullMatch = []

    # Check for all possible combinations against the soup
    print("Checking " + str(wordCount) + '-word combinations...')
    lenCombos = vol.splitOptions(len(sortedSoup), wordCount)
    print(lenCombos)
    setList = vol.generateCandidates(lenCombos, worddb)
    setCount = len(setList)

    if setList:
        print("setList length: " + str(setCount))

    lock = asyncio.Lock()
    progress = [1, setCount]

    for entry in setList:
        asyncio.ensure_future(vol.processSet(sortedSoup, entry,
                                             lock, fullMatch, progress))

    return fullMatch

if __name__ == "__main__":
    main(sys.argv)
