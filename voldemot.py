"""
voldemot

Takes a set of letters (such as a name) and assembles combinations of words based on it.
Using English word list from SCOWL.
The results are output to a text file: [input]-iter.txt

Usage:
python voldemot letters [filename] [slots]

For example,
python voldemot.py albertcamus words/voldemot-dict.txt 2

will yield a text file called albert-camus.iter with 113
combinations, from "ablate scrum" to "tsamba ulcer".
"""

import sys
import re
import time
from collections import Counter
import asyncio
import voldemot_utils as vol

def main(args):
    """ main program """
    # for i in enumerate(args):
        # print(i)

    if len(args) < 2:
        print("Not enough arguments.\nUsage:\npython name-scrambler letters [filename]")

    # load source soup
    letters = args[1]

    # remove spaces and non-alphabetical characters
    letters = re.sub(r"\W?\d?", "", letters).lower()

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
    wordsFound = vol.getWordList(wordFileName, letters)
    print("Found " + str(len(wordsFound)) + " words.")

    start = time.time()

    fullMatch = []
    # # generate all possible and put them in the fullMatch list
    loop = asyncio.get_event_loop()
    if wordCount == 4:
        fullMatch = loop.run_until_complete(fourWordCombinations(wordsFound, letters))
    elif wordCount == 3:
        fullMatch = loop.run_until_complete(threeWordCombinations(wordsFound, letters))
    elif wordCount == 2:
        fullMatch = loop.run_until_complete(twoWordCombinations(wordsFound, letters))
    else:
        # Default to single words:
        for word in vol.getWordsEqualTo(wordsFound, len(letters)):
            if sorted(word) == sorted(letters):
                fullMatch.append(word)
    loop.close()
    end = time.time()
    print(f"{(end-start):.2f} seconds elapsed.")
    print(f"There are {len(fullMatch)} full matches.")

    for entry in fullMatch:
        print(entry)

async def wordCombinationsRec(wordsFound, targetMatch, spotsLeft, matchList, baggage=''):
    """ find all word combinations given a list and length using recursion """
    if spotsLeft == 1:
        # One word left
        for word in vol.getWordsEqualTo(wordsFound, len(targetMatch) - len(baggage)):
            tempCombo = baggage + word
            if sorted(tempCombo) == sorted(targetMatch):
                matchList.append(tempCombo)
    else:
        trimmedList = wordsFound.copy()
        if not baggage:
            total = 0
        for word in vol.getWordsUnder(trimmedList, len(targetMatch) - len(baggage) - (spotsLeft-2)):
            if not baggage:
                total += 1
            tempCombo = baggage + word
            if vol.wordIsPresent(tempCombo, targetMatch):
                await wordCombinationsRec(trimmedList, targetMatch, spotsLeft-1,
                                          matchList, tempCombo)
            trimmedList.remove(word)
            if not baggage:
                print(f"{(total * 100)/len(wordsFound):.2f}% done.")

async def twoWordCombinations(wordsFound, letters):
    """ return a list of two-word combinations """
    fullMatch = []
    firstList = wordsFound.copy()
    total = 0
    for first in wordsFound:
        total += 1
        for second in vol.getWordsEqualTo(firstList, len(letters) - len(first)):
            testCombo = first + second
            if sorted(testCombo) == sorted(letters):
                fullMatch.append(f"{first} {second}")
        firstList.remove(first)
    return fullMatch

async def threeWordCombinations(wordsFound, letters):
    """ return a list of three-word combinations """
    fullMatch = []
    firstList = wordsFound.copy()
    total = 0
    for first in vol.getWordsUnder(firstList, len(letters) - 2):
        total += 1
        secondList = firstList.copy()
        for second in vol.getWordsUnder(secondList, len(letters) - len(first)):
            twoWordCombo = first + second
            if vol.wordIsPresent(twoWordCombo, letters):
                thirdList = secondList.copy()
                for third in vol.getWordsEqualTo(thirdList, len(letters) - len(twoWordCombo)):
                    testCombo = twoWordCombo + third
                    if sorted(testCombo) == sorted(letters):
                        fullMatch.append(f"{first} {second} {third}")
            secondList.remove(second)
        firstList.remove(first)
    return fullMatch

async def fourWordCombinations(wordsFound, letters):
    """ return a list of four-word combinations """
    fullMatch = []
    total = 0
    firstList = wordsFound.copy()
    for first in vol.getWordsUnder(firstList, len(letters) - 3):
        total += 1
        secondList = firstList.copy()
        for second in vol.getWordsUnder(secondList, len(letters) - len(first) - 2):
            twoWordCombo = first + second
            if vol.wordIsPresent(twoWordCombo, letters):
                thirdList = secondList.copy()
                for third in vol.getWordsUnder(thirdList, len(letters) - len(twoWordCombo)):
                    threeWordCombo = twoWordCombo + third
                    if vol.wordIsPresent(threeWordCombo, letters):
                        fourthList = thirdList.copy()
                        for fourth in vol.getWordsEqualTo(fourthList, len(letters) - len(threeWordCombo)):
                            fourWordCombo = threeWordCombo + fourth
                            if sorted(fourWordCombo) == sorted(letters):
                                fullMatch.append(f"{first} {second} {third} {fourth}")
                    thirdList.remove(third)
            secondList.remove(second)
        firstList.remove(first)
    return fullMatch

def voldemot(letters, wordCount):
    """ simplified function call that always goes to the standard dictionary """
    # remove spaces and non-alphabetical characters
    letters = re.sub(r"\W?\d?", "", letters).lower()
    letters = letters[:16]

    wordList = vol.getWordList("words/voldemot-dict.txt", letters)
    if wordCount == 4:
        fullMatch = fourWordCombinations(wordList, letters)
    elif wordCount == 3:
        fullMatch = threeWordCombinations(wordList, letters)
    elif wordCount == 2:
        fullMatch = twoWordCombinations(wordList, letters)
    else:
        # Default to single words:
        for word in vol.getWordsEqualTo(wordList, len(letters)):
            if sorted(word) == sorted(letters):
                fullMatch.append(word)
    return letters, fullMatch

if __name__ == "__main__":
    main(sys.argv)
