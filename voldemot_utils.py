"""
voldemot_utils
Helper functions for voldemot package
"""
import asyncio
import json
from itertools import combinations, chain, product

def loadDictionary(filename):
    """ reads words line by line from a file and returns them in a list """
    # wordList = []
    wordFile = open(filename, "r")
    wordList = [word.rstrip().lower() for word in wordFile if "'" not in word]
    wordFile.close()
    print("Read " + str(len(wordList)) + " words.")
    return wordList

def wordIsPresent(word, soup):
    """ checks if the word can be assembled with the characters in the soup """
    testWord = word
    for letter in soup:
        testWord = testWord.replace(letter,"",1)
    return not testWord

def findWords(wordsFileName, letters, worddb):
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
            worddb.query("INSERT INTO words VALUES ('" + word + "'," + str(len(word)) + ")")
            worddb.commit()

    return wordsFound

def sumToN(n):
    'Generate the series of +ve integer lists which sum to a +ve integer, n.'
    from operator import sub
    b, mid, e = [0], list(range(1, n)), [n]
    splits = (d for i in range(n) for d in combinations(mid, i))

    return set((tuple(sorted(list(map(sub, chain(s, e), chain(b, s))))) for s in splits))

def splitOptions(wordlength, count):
    'Returns the available combinations for the word length and number of words'
    return sorted(list((option for option in sumToN(wordlength) if len(option) == count)))

def getWordsOfLength(wordLength, worddb):
    'Returns a list of words from the database matching the required length.'
    return [word[0] for word in worddb.query("SELECT word FROM words WHERE length IS " + str(wordLength))]

def genSetList(lenCombos, worddb):
    """
    Generate word sets based on word lengths provided by lenCombos:
    Get only the words that match the lengths in this list
    lenCombo is a tuple of the possible length combinations
    that add up to letterCount
    """
    return [[getWordsOfLength(length, worddb) for length in lenCombo] for lenCombo in lenCombos]

async def processSet(sortedSoup, wordSet, lock, fullMatch, progress):
    """
    Compares a set of words to the sorted letters and returns all matches.
    """
    comboSet = []
    for combo in product(*wordSet):
        sortedCombo = sorted(combo)
        letterList = sorted([letter for word in combo for letter in word])
        if sortedSoup == letterList and sortedCombo not in comboSet:
            comboSet.append(sortedCombo)

    with await lock:
        fullMatch.extend(comboSet)
        print(f"Progress: {int(progress[0]*(100/progress[1])):3}%")
        progress[0] += 1

    # if len(wordSet) > 3:
    #     await asyncio.sleep(0.5)
    # else:
    #     await asyncio.sleep(0.25)
