"""
voldemot

Takes a set of letters (such as a name) and assembles combinations of words based on it.
Using English word list from SCOWL.

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

    if len(args) < 2:
        print("Not enough arguments.\nUsage:\npython voldemot.py letters [filename]")

    # load source soup
    letters = args[1]

    # remove spaces and non-alphabetical characters
    letters = re.sub(r"\W?\d?", "", letters).lower()
    print("Source soup (" + letters + ") has " + str(len(letters)) + " characters")

    # generate dictionary file name
    wordFileName = "words/voldemot-dict.txt"
    if len(args) > 3:
        wordFileName = args[2]

    # set number of spots
    wordCount = 3
    if len(args) > 3:
        wordCount = int(args[3])

    # make a list of candidate words
    wordsFound = vol.searchDictionary(wordFileName, letters)
    print("Found " + str(len(wordsFound)) + " words.")

    start = time.time()

    fullMatch = []
    # # generate all possible and put them in the fullMatch list
    loop = asyncio.get_event_loop()
    if wordCount >= 2:
        fullMatch = loop.run_until_complete(vol.findWordCombinations(wordsFound, letters, wordCount, 10000, 0.05))
    else:
        # Default to single words:
        for word in vol.getWordsEqualTo(wordsFound, len(letters)):
            if sorted(word) == sorted(letters):
                fullMatch.append(word)
    loop.close()
    end = time.time()
    print(f"{(end-start):.2f} seconds elapsed.")
    print(f"There are {len(fullMatch)} full matches.")

    # for entry in fullMatch:
        # print(entry)

if __name__ == "__main__":
    main(sys.argv)
