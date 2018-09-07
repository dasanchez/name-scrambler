"""
voldemot_utils
Helper functions for voldemot package
"""
import asyncio
import json
from itertools import combinations, chain, product

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

def sumToN(n):
    'Generate the series of +ve integer lists which sum to a +ve integer, n.'
    from operator import sub
    b, mid, e = [0], list(range(1, n)), [n]
    splits = (d for i in range(n) for d in combinations(mid, i))
    return (list(map(sub, chain(s, e), chain(b, s))) for s in splits)

def splitOptions(wordlength, count):
    'Returns the available combinations for the word length and number of words'
    options = []
    for s in sumToN(wordlength):
        s = sorted(s)
        if (len(s) == count and s not in options):
            options.append(s)
    return options

def genSetList(lenCombos, worddb):
    'Generate word sets based on word lengths provided by lenCombos'
    setList = []
    for lenCombo in lenCombos:
        # Get only the words that match the lengths in this list
        # lenCombo is a tuple of the possible length combinations
        # that add up to letterCount
        comboList = []
        for length in lenCombo:
            wordSet = []
            for word in worddb.query("SELECT word FROM words WHERE length IS " + str(length)):
                wordSet.append(word[0])
            comboList.append(wordSet)
        setList.append(comboList)
    return setList

async def processSet(sortedSoup, wordSet, lock, fullMatch, progress):
    """
    Compares a set of words to the sorted letters and returns all matches.
    """
    comboSet = []
    for combo in product(*wordSet):
        letterList = sorted([letter for word in combo for letter in word])
        if sortedSoup == letterList and sorted(combo) not in comboSet:
            comboSet.append(sorted(combo))
    # print(f"Coroutine {proc_id} finished")
    with await lock:
        fullMatch.extend(comboSet)
        print(f"Progress: {int(progress[0]*(100/progress[1])):3}%")
        progress[0] += 1

async def processClientSet(sortedSoup, wordSet, lock, fullMatch, progress, ws):
    """
    Compares a set of words to the sorted letters and returns all matches.
    """
    comboSet = []
    for combo in product(*wordSet):
        letterList = sorted([letter for word in combo for letter in word])
        if sortedSoup == letterList and sorted(combo) not in comboSet:
            comboSet.append(sorted(combo))

    with await lock:
        for combo in comboSet:
            response = json.dumps({'match': True, 'value': combo})
            await (ws.send(response))        
        fullMatch.extend(comboSet)
        percent = int(progress[0]*(100/progress[1]))
        print(f"Progress: {percent:3}%")
        response = json.dumps({'percent': True, 'value': percent})
        await ws.send(response)
        progress[0] += 1
            

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

