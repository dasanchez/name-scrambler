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

def main(args):
    """ main program """
    if len(args) < 2:
        print("Not enough arguments.\nUsage:\npython name-scrambler letters [filename]")

    # load source soup
    letters = args[1]
    sortedLetters = sorted(list(letters))
    print("Source soup (" + letters + ") has " + str(len(letters)) + " characters")

    # generate dictionary file name
    wordFileName = "words/voldemot-dict.txt"
    if len(args) > 2:
        wordFileName = args[2]

    # set number of slots
    wordCount = 3
    if len(args) > 3:
        wordCount = int(args[3])

    # find words present in the soup
    wordsFound = findWords(wordFileName, letters)
    print("Found " + str(len(wordsFound)) + " words in the soup.")

    # generate all possible and put them in the fullMatch list
    fullMatch = fillBucket(sortedLetters, wordsFound, wordCount)

    print("There are " + str(len(fullMatch)) + " full matches")

    outFileName = "words/" + letters + "-iter.txt"

    outFile = open(outFileName, "w")
    for entry in fullMatch:
        myStr = ""
        for word in entry:
            myStr = myStr + word + " "
        outFile.write(myStr.rstrip(" ") + "\n")
    outFile.close()

def voldemot(letters, wordsRequested):
    """ simplified function call that always goes to the standard dictionary """
    wordsFound = findWords("words/voldemot-dict.txt", letters)
    fullMatch = fillBucket(sorted(letters), wordsFound, wordsRequested)
    return fullMatch

def fillBucket(sortedSoup, wordsFound, wordCount):
    """ populate fullMatch list """
    fullMatch = []
    letterCount = len(sortedSoup)

    # Check for all possible combinations against the soup
    for i in range(1, wordCount+1):
        print("Checking " + str(i) + "-word combinations...")
        for combo in itertools.combinations(wordsFound, i):

            letterList = []
            for word in combo:
                letterList.extend(word)

            if len(letterList) == letterCount:
                if sortedSoup == sorted(letterList):
                    if combo not in fullMatch:
                        fullMatch.append(combo)

    return fullMatch

def findWords(wordsFileName, letters):
    """ fills wordsFound list with words found in the letters string """
    wordsFound = []
    soupFileName = "words/" + letters + ".txt"

    if os.path.isfile(soupFileName):
        # File exists
        soupFile = open(soupFileName, "r")
        print("Reading from file " + soupFileName + "...")
        for line in soupFile:
            wordsFound.append(line.rstrip())
        soupFile.close()
    else:
        # File does not exist
        # load dictionary
        wordList = loadDictionary(wordsFileName)
        soupFile = open(soupFileName, "w")
        print("Saving to file " + soupFileName + "...")
        # Check if a word can be assembled from the letters available.
        # If so, add it to the wordsFound list.
        for word in wordList:
            if wordIsPresent(word, letters):
                wordsFound.append(word)
                soupFile.write(word + "\n")
        soupFile.close()
    
    return wordsFound

def loadDictionary(filename):
    """ reads words line by line from a file and returns them in a list """
    wordList = []
    wordFile = open(filename, "r")
    for word in wordFile:
        if "'" not in word:
            wordList.append(word.rstrip().lower())
    wordFile.close()
    print("Read " + str(len(wordList)) + " words.")
    return wordList

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
