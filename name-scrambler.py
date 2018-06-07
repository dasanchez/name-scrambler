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
        print(
            "Not enough arguments.\nUsage:\npython name-scrambler letters [filename]")

    # load source soup
    letters = args[1]
    soupFileName = "words/" + letters + ".txt"
    
    wordsFound = []
    if os.path.isfile(soupFileName):
        # File exists
        soupFile = open(soupFileName,"r")
        print("Reading from file " + soupFileName + "...")
        for line in soupFile:
            wordsFound.append(line.rstrip())
        soupFile.close()
    else:
        # File does not exist
        # load dictionary
        if len(args) > 2:
            wordList = loadWords(args[2])
        else:
            wordList = loadWords("words/full-list.txt")

        soupFile = open(soupFileName,"w")
        print("Saving to file " + soupFileName + "...")
        # Check if a word can be assembled from the letters available.
        # If so, add it to the wordsFound list.
        for word in wordList:
            if wordIsPresent(word, letters):
                wordsFound.append(word)
                soupFile.write(word + "\n")
        soupFile.close()

    print("Found " + str(len(wordsFound)) + " words in the soup.")

    # Check for all remaining words after removing each word from the soup.
    combo1 = []

    for word in wordsFound:
        # iterate through each word as the starter
        testLetters = letters[:]

        for letter in word:
            testLetters = testLetters.replace(letter, "", 1)

        for testWord in wordsFound:
            currentCombo = [word]
            if testWord not in currentCombo:
                #print("Next test word: " + testWord)
                if wordIsPresent(testWord, testLetters):
                    currentCombo.append(testWord)
                    combo1.append(currentCombo)
                    #print("Testing for word " + word + ", letters "
                    #  + testLetters + ": " + str(wordCombo))
                    # for letter in testWord:
                        # testLetters = testLetters.replace(letter, "", 1)

    print("Two-item list has " + str(len(combo1)) + " entries:")
    print(str(combo1[:int(len(combo1)):int(len(combo1)/10)]))

    combo2 = []
    for entry in combo1:
        # iterate through each combo1 entry as the starter
        testLetters = letters[:]
        for word in entry:
            for letter in word:
                testLetters = testLetters.replace(letter,"",1)
        
        for testWord in wordsFound:
            currentCombo = entry[:]
            if testWord not in currentCombo:
                if wordIsPresent(testWord, testLetters):
                    currentCombo.append(testWord)
                    combo2.append(currentCombo)

    print("Three-item list has " + str(len(combo2)) + " entries:")
    print(str(combo2[:int(len(combo2)):int(len(combo2)/10)]))

    combo3 = []
    for entry in combo2:
        # iterate through each combo1 entry as the starter
        testLetters = letters[:]
        for word in entry:
            for letter in word:
                testLetters = testLetters.replace(letter,"",1)
        
        for testWord in wordsFound:
            currentCombo = entry[:]
            if testWord not in currentCombo:
                if wordIsPresent(testWord, testLetters):
                    currentCombo.append(testWord)
                    combo3.append(currentCombo)

    print("Four-item list has " + str(len(combo3)) + " entries:")
    print(str(combo3[:int(len(combo3)):int(len(combo3)/10)]))

    # print("Combinations that used all letters:")
    # for entry in combinations:
    #     print(str(entry))


def loadWords(filename):
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
