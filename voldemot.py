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

    # wordDict = { word: len(word) for word in wordsFound }

    start = time.time()

    # print("1-word matches:")
    # for word in getWordsOfLength(wordDict, len(letters)):
    #     if sorted(letters) == sorted(word):
    #         fullMatch.append(word)

    # # generate all possible and put them in the fullMatch list
    loop = asyncio.get_event_loop()
    # fullMatch = loop.run_until_complete(generateList(sortedLetters, wordCount, worddb))
    fullMatch = loop.run_until_complete(fourWordCombinations(wordsFound, letters))
    # loop.close()

    end = time.time()
    print(f"{(end-start):.2f} seconds elapsed.")
    print(f"There are {len(fullMatch)} full matches.")

    # for entry in fullMatch:
        # print(entry)

    start = time.time()
    # generate all possible and put them in the fullMatch list
    loop = asyncio.get_event_loop()
    fullMatch = loop.run_until_complete(generateList(sortedLetters, wordCount, worddb))
    loop.close()

    end = time.time()
    print(f"{(end-start):.2f} seconds elapsed")
    print("There are " + str(len(fullMatch)) + " full matches.")

    # for entry in fullMatch:
    #     myStr = ""
    #     for word in entry:
    #         myStr = myStr + word + " "
    #     print(myStr)

async def twoWordCombinations(wordsFound, letters):
    """ return a list of two-word combinations """
    fullMatch = []
    firstList = wordsFound.copy()
    total = 0
    for first in wordsFound:
        total += 1
        for second in getWordsEqualTo(firstList, len(letters) - len(first)):
            testCombo = first + second
            if sorted(testCombo) == sorted(letters):
                # await asyncio.sleep(0.05)
                fullMatch.append(f"{first} {second}")
        firstList.remove(first)
        print(f"{(total * 100)/len(wordsFound):.2f}% done.")
    return fullMatch

async def threeWordCombinations(wordsFound, letters):
    """ return a list of three-word combinations """
    fullMatch = []
    firstList = wordsFound.copy()
    total = 0
    for first in getWordsUnder(firstList, len(letters) - 2):
        total += 1
        secondList = firstList.copy()
        for second in getWordsUnder(secondList, len(letters) - len(first)):
            twoWordCombo = first + second
            if vol.wordIsPresent(twoWordCombo, letters):
                thirdList = secondList.copy()
                for third in getWordsEqualTo(thirdList, len(letters) - len(twoWordCombo)):
                    testCombo = twoWordCombo + third
                    if sorted(testCombo) == sorted(letters):
                        fullMatch.append(f"{first} {second} {third}")
            secondList.remove(second)
        firstList.remove(first)
        print(f"{(total * 100)/len(wordsFound):.2f}% done.")
    return fullMatch

async def fourWordCombinations(wordsFound, letters):
    """ return a list of four-word combinations """
    pauseInterval = 10000
    pauseLength = 0.1
    fullMatch = []
    total = 0
    intervalCounter = 0
    firstList = wordsFound.copy()
    for first in getWordsUnder(firstList, len(letters) - 3):
        # print(f"Word {total}: {first}")
        total += 1
        secondList = firstList.copy()
        for second in getWordsUnder(secondList, len(letters) - len(first) - 2):
            twoWordCombo = first + second
            if vol.wordIsPresent(twoWordCombo, letters):
                thirdList = secondList.copy()
                for third in getWordsUnder(thirdList, len(letters) - len(twoWordCombo)):
                    threeWordCombo = twoWordCombo + third
                    if vol.wordIsPresent(threeWordCombo, letters):
                        fourthList = thirdList.copy()
                        for fourth in getWordsEqualTo(fourthList, len(letters) - len(threeWordCombo)):
                            fourWordCombo = threeWordCombo + fourth
                            if sorted(fourWordCombo) == sorted(letters):
                                fullMatch.append(f"{first} {second} {third} {fourth}")
                            # intervalCounter += 1
                            # if intervalCounter == pauseInterval:
                                # await asyncio.sleep(pauseLength)
                                # intervalCounter = 0
                    thirdList.remove(third)
            secondList.remove(second)
        firstList.remove(first)
        print(f"{(total * 100)/len(wordsFound):.2f}% done.")
    return fullMatch

def getWordsEqualTo(wordList, targetLength):
    """ return list of words of a specified length in the list """
    return [word for word in wordList if len(word) == targetLength]

def getWordsUnder(wordList, targetLength):
    """ return list of words of a specified length in the list """
    return [word for word in wordList if len(word) < targetLength]

def getWords(wordList, targetLength):
    """ return list of words of a specified length in the list """
    return [word for word in wordList if len(word) <= targetLength]

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
