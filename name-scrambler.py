"""
name-scrambler

Takes a set of letters (such as a name) and assembles combinations of words based on it.
Using English word list from SCOWL.

Usage:
python name-scrambler letters [filename]
"""

import itertools
import sys

def main(args):
    if len(args) < 2:
        print("Not enough arguments.\nUsage:\npython name-scrambler letters [filename]")

    # load source soup
    letters = args[1]

    # load dictionary
    if len(args) > 2:
        wordList = loadWords(args[2])
    else:
        wordList = loadWords("words/full-list.txt")
    
    # Check if a word can be assembled from the letters available.
    # If so, add it to the wordsFound list.
    wordsFound = []
    for word in wordList:
        wordsFound.append(word) if wordIsPresent(word, letters) else True

    print("Found " + str(len(wordsFound)) + " words. First ten:")
    for word in wordsFound[:10]:
        print(word)

    # Check for all remaining words after removing each word from the soup.
    combinations = []

    for word in wordsFound:
        # iterate through each word as the starter
        testLetters = letters[:]
        wordCombo = [word]
        for letter in word:
            testLetters = testLetters.replace(letter,"",1)
        counter = 0
        for testWord in wordsFound:
            if testWord not in wordCombo:
                #print("Next test word: " + testWord)
                if wordIsPresent(testWord, testLetters) and len(testWord)>=5:
                    wordCombo.append(testWord)
                    #print("Testing for word " + word + ", letters " + testLetters + ": " + str(wordCombo))
                    for letter in testWord:
                        testLetters = testLetters.replace(letter,"",1)
                else:
                    counter += 1
            if counter >= len(wordsFound):
                break
        if len(testLetters) == 0:
            combinations.append(wordCombo)

    print("Combinations that used all letters:")
    for entry in combinations:
        print(str(entry))

def loadWords(filename):
    wordList = []
    wordFile = open(filename, "r")
    for word in wordFile:
        if "'" not in word:
            wordList.append(word.rstrip().lower())
    wordFile.close()
    print("Read " + str(len(wordList))+ " words.")
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

if __name__ == "__main__": main(sys.argv)



