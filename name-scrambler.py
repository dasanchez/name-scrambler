"""
name-scrambler

Takes a set of letters (such as a name) and assembles combinations of words based on it.
Using English word list from SCOWL.

Usage:
python name-scrambler letters [filename]
"""

# import itertools
import sys
import os.path

def main(args):
    """ main program """
    if len(args) < 2:
        print("Not enough arguments.\nUsage:\npython name-scrambler letters [filename]")

    # load source soup
    letters = args[1]
    print("Source soup has " + str(len(letters)) + " characters")

    wordFileName = "words/full-list.txt"
    if len(args) > 2:
        wordFileName = args[2]

    wordsFound = []
    findWords(wordFileName, wordsFound, letters)
    print("Found " + str(len(wordsFound)) + " words in the soup.")

    fullMatch = []
    # Check for all remaining words after removing each word from the soup.
    combo1 = []
    for word in wordsFound:
        # iterate through each word as the starter
        testLetters = letters[:]

        # prepare temporary test soup
        for letter in word:
            testLetters = testLetters.replace(letter, "", 1)

        for testWord in wordsFound:
            currentCombo = {word}
            if testWord not in currentCombo:
                if wordIsPresent(testWord, testLetters):
                    currentCombo.add(testWord)
                    # Two scenarios: 
                    # 1. we have a full match (number of letters)
                    # 2. we can fit more words
                    if currentCombo not in combo1 and currentCombo not in fullMatch:
                        if isfullMatch(currentCombo, letters):
                            fullMatch.append(currentCombo)
                            print(str(currentCombo))
                        elif hasPotentialAdditions(currentCombo, testLetters, wordsFound):
                            combo1.append(currentCombo)

    print("Two-item list has " + str(len(combo1)) + " entries")
    print("There are " + str(len(fullMatch)) + " full matches")

    combo2 = []
    for entry in combo1:
        # iterate through each combo1 entry as the starter
        testLetters = letters[:]
        for word in entry:
            
            # prepare temporary test soup
            for letter in word:
                testLetters = testLetters.replace(letter,"",1)
        
        # iterate through the remaining words
        for testWord in wordsFound:
            currentCombo = set(entry)
            if testWord not in currentCombo:
                if wordIsPresent(testWord, testLetters):
                    currentCombo.add(testWord)
                    # Two scenarios: 
                    # 1. we have a full match (number of letters)
                    # 2. we can fit more words
                    if currentCombo not in combo2 and currentCombo not in fullMatch:
                        if isfullMatch(currentCombo, letters):
                            fullMatch.append(currentCombo)
                            print(str(currentCombo))
                        elif hasPotentialAdditions(currentCombo, testLetters, wordsFound):
                            combo2.append(currentCombo)

    print("Three-item list has " + str(len(combo2)) + " entries")
    print("There are " + str(len(fullMatch)) + " full matches")

    combo3 = []
    for entry in combo2:
        # iterate through each combo1 entry as the starter
        testLetters = letters[:]
        for word in entry:
            
            # prepare temporary test soup
            for letter in word:
                testLetters = testLetters.replace(letter,"",1)
        
        # iterate through the remaining words
        for testWord in wordsFound:
            currentCombo = set(entry)
            if testWord not in currentCombo:
                if wordIsPresent(testWord, testLetters):
                    currentCombo.add(testWord)
                    # Two scenarios: 
                    # 1. we have a full match (number of letters)
                    # 2. we can fit more words
                    if currentCombo not in combo3 and currentCombo not in fullMatch:
                        if isfullMatch(currentCombo, letters):
                            fullMatch.append(currentCombo)
                            print(str(currentCombo))
                        elif hasPotentialAdditions(currentCombo, testLetters, wordsFound):
                            combo3.append(currentCombo)

    print("Four-item list has " + str(len(combo3)) + " entries")
    print("There are " + str(len(fullMatch)) + " full matches")

    outFileName = "words/" + letters + "-out.txt"

    outFile = open(outFileName, "w")
    for entry in fullMatch:
        outFile.write(str(entry) + "\n")
    outFile.close()

def hasPotentialAdditions(words, soup, wordsFound):
    """ check if there are matches in the remainder of the bag of words """
    validCombo = False
    for nextWord in wordsFound:
        if nextWord not in words:
            if wordIsPresent(nextWord, soup):
                validCombo = True
                break
    if validCombo:
        return True
    else:
        return False

def isfullMatch(words, letters):
    """ check if we have used up all of the letters """
    counter = 0
    for entry in words:
        for word in entry:
            counter += len(word)
    if counter >= len(letters):
            return True
    else:
        return False

def findWords(wordsFileName, wordsFound, letters):
    """ fills wordsFound list with words found in the letters string """
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
