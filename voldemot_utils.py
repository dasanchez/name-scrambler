from itertools import combinations, chain

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
    setList = []
    for lenCombo in lenCombos:
        # Get only the words that match the lengths in this list
        # lenCombo is a tuple of the possible length combinations 
        # that add up to letterCount
        comboList = []
        # print("\nlenCombo "+ str(lenCombo)+":")
        for length in lenCombo:
            # print(str(length) + "-letter words:")
            wordSet = []
            for word in worddb.query("SELECT word FROM words WHERE length IS " + str(length)):
                wordSet.append(word[0])
            comboList.append(wordSet)
        setList.append(comboList)
    return setList