"""
voldemot

Takes a set of letters (such as a name) and assembles combinations of words based on it.
Using English word list from SCOWL.
The results are output to a text file: [input]-iter.txt

Usage:
python voldemot letters [filename] [slots]

For example,
python voldemot albertcamus words/voldemot-dict.txt 2

will yield a text file called albert-camus.iter with 1125
combinations, "a clubmaster" and "cabal muster" to
"macabre slut" and "tsamba ulcer".
"""

import itertools
import sys
import os.path
from voldemot_utils import *
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
    sortedLetters = sorted(list(letters))
    # print("Sorted letters: " + str(sortedLetters))
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
    wordsFound = findWords(wordFileName, letters, worddb)
    print("Found " + str(len(wordsFound)) + " words in the soup.")

    # generate all possible and put them in the fullMatch list
    fullMatch = fillBucket(sortedLetters, wordsFound, wordCount, worddb)

    print("There are " + str(len(fullMatch)) + " full matches")

    # outFileName = "words/" + letters + "-iter-" + str(wordCount) + ".txt"

    # outFile = open(outFileName, "w")
    for entry in fullMatch:
        myStr = ""
        for word in entry:
            myStr = myStr + word + " "
        print(myStr)
        # outFile.write(myStr.rstrip(" ") + "\n")
    # outFile.close()

def voldemot(letters, wordsRequested):
    """ simplified function call that always goes to the standard dictionary """
    worddb = wordDB.wordDB()
    worddb.query("CREATE TABLE words(word text, length int)")

    wordsFound = findWords("words/voldemot-dict.txt", letters,worddb)
    fullMatch = fillBucket(sorted(letters), wordsFound, wordsRequested, worddb)
    return fullMatch

def fillBucket(sortedSoup, wordsFound, wordCount, worddb):
    """ populate fullMatch list """
    fullMatch = []
    letterCount = len(sortedSoup)

    # Check for all possible combinations against the soup
    print("Checking " + str(wordCount) + '-word combinations...')
    lenCombos = splitOptions(letterCount, wordCount)
    print(lenCombos)
    setList = genSetList(lenCombos, worddb)
    if (len(setList)):
        print("setList length: " + str(len(setList)))
        if (len(setList) == 1):
            print(setList[0])

    for entry in setList:
        for combo in itertools.product(*entry):
            letterList = sorted([letter for word in combo for letter in word])

            if sortedSoup == letterList:
                if combo not in fullMatch:
                    fullMatch.append(combo)

    return fullMatch

def findWords(wordsFileName, letters, worddb):
    """
    Fills wordsFound list with words found in the letters string.
    wordfound is a dictionary with a word as a key and the length as a value
    """
    wordsFound = []
    # soupFileName = "words/" + letters + ".txt"

    # Load dictionary and save to file
    wordList = loadDictionary(wordsFileName)
    # soupFile = open(soupFileName, "w")
    # print("Saving to file " + soupFileName + "...")

    # Check if a word can be assembled from the letters available.
    # If so, add it to the wordsFound list.
    for word in wordList:
        if wordIsPresent(word, letters):
            wordsFound.append(word)
            # query = "INSERT INTO words VALUES ('" + word + "'," + str(len(word)) + ")"
            # print(query)
            worddb.query("INSERT INTO words VALUES ('" + word + "'," + str(len(word)) + ")")
            worddb.commit()
            # soupFile.write(word + "\n")
        # soupFile.close()

    return wordsFound

def wordIsPresent(word, soup):
    """ checks if the word can be assembled with the characters in the soup """
    wordOK = True
    tempLetters = soup[:]
    for letter in word:
        if letter not in tempLetters:
            wordOK = False
            break
        else:
            tempLetters = tempLetters.replace(letter, "", 1)
    return wordOK

if __name__ == "__main__":
    main(sys.argv)
