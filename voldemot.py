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

# import itertools
import sys
import re
import time
import asyncio
# from multiprocessing import Process, Queue
import voldemot_utils as vol
import wordDB

def main(args):
    """ main program """
    start = time.time()

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
    wordsFound = vol.findWords(wordFileName, letters, worddb)
    print("Found " + str(len(wordsFound)) + " words.")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(fillBucket(sortedLetters, wordCount, worddb))
    loop.close()
    # generate all possible and put them in the fullMatch list
    # fullMatch = fillBucket(sortedLetters, wordCount, worddb)
    # print("There are " + str(len(fullMatch)) + " full matches")

    # for entry in fullMatch:
    #     myStr = ""
    #     for word in entry:
    #         myStr = myStr + word + " "
    #     print(myStr)

    end = time.time()
    print(str(int(end-start)) + " seconds elapsed")

def voldemot(letters, wordsRequested):
    """ simplified function call that always goes to the standard dictionary """
    worddb = wordDB.wordDB()
    worddb.query("CREATE TABLE words(word text, length int)")

    # remove spaces and non-alphabetical characters
    letters = re.sub(r"\W?\d?", "", letters).lower()
    letters = letters[:16]

    vol.findWords("words/voldemot-dict.txt", letters, worddb)
    fullMatch = fillBucket(sorted(letters), wordsRequested, worddb)
    return letters, fullMatch

async def fillBucket(sortedSoup, wordCount, worddb):
    """ populate fullMatch list """
    # CHUNKSIZE = 4
    fullMatch = []

    # Check for all possible combinations against the soup
    print("Checking " + str(wordCount) + '-word combinations...')
    lenCombos = vol.splitOptions(len(sortedSoup), wordCount)
    print(lenCombos)
    setList = vol.genSetList(lenCombos, worddb)
    setCount = len(setList)

    if setList:
        print("setList length: " + str(setCount))
        if setCount == 1:
            print(setList[0])

    progress = 1
    id = 1

    tasks = []
    for entry in setList:
        tasks.append(asyncio.ensure_future(vol.processSet(id, sortedSoup, entry)))
        id += 1
        # setCombos = []
        # for combo in vol.processSet(sortedSoup, entry):
            # if combo not in setCombos:
                # setCombos.append(combo)
        # fullMatch.extend(setCombos)
        # print(f"{lenCombos[progress-1]} | {len(setCombos):4} | " +
            #   f"{int(progress*(100/setCount)):3}%")
        # for combo in setCombos:
            # print(combo)
        # progress += 1

    await asyncio.gather(*tasks)

    return fullMatch

# def processSet(sortedSoup, wordSet, q):

if __name__ == "__main__":
    main(sys.argv)
