"""
voldemot - a word de-scrambler by @dasanchez

Usage:
usage: voldemot.py [-h] [-d DICTIONARY] [-c COUNT] [-v] [-p] input

positional arguments:
  input                 the letters to de-scramble

optional arguments:
  -h, --help
                        show this help message and exit
  -d DICTIONARY, --dictionary DICTIONARY
                        dictionary file: newline must separate all words
                        default: words/voldemot-dict.txt
  -c COUNT, --count COUNT
                        number of words to split the letters into
                        default: 2
  -v, --verbose
                        show progress
  -p, --print
                        print results
  -o, -- output                        
                        save results to file
                        default: voldemot.txt

For example,
python voldemot.py albertcamus -d words/voldemot-dict.txt -c 3 -p
will print 113 combinations, from "ablate scrum" to "tsamba ulcer".
"""
import re
import time
import argparse
import asyncio
import voldemot_utils as vol

def main(args):
    """ main program """
    # load source soup
    letters = args.input

    # remove spaces and non-alphabetical characters
    letters = re.sub(r"\W?\d?", "", letters).lower()
    if args.verbose:
        print("Source soup (" + letters + ") has " +
              str(len(letters)) + " characters")

    # generate dictionary file name
    wordFileName = args.dictionary

    # set number of spots
    wordCount = args.count

    # make a list of candidate words
    wordsFound = vol.getWordList(wordFileName, letters)
    if args.verbose:
        print("Found " + str(len(wordsFound)) + " words.")

    start = time.time()

    fullMatch = []
    # generate all possible and put them in the fullMatch list
    loop = asyncio.get_event_loop()
    if wordCount >= 2:
        fullMatch = loop.run_until_complete(vol.findWordCombinations(
            wordsFound, letters, wordCount, 10000, 0.05, args.verbose))
    else:
        # Default to single words:
        for word in vol.getWordsEqualTo(wordsFound, len(letters)):
            if sorted(word) == sorted(letters):
                fullMatch.append(word)
    loop.close()
    end = time.time()

    print(f"{(end-start):.2f} seconds elapsed, there are {len(fullMatch)} full matches.")

    if args.output:
        if args.verbose:
            print(f"Saving results to {args.output}...")
        f = open(args.output, "w")

    for entry in fullMatch:
        if args.print:
            print(entry)
        if args.output:
            f.write(entry + "\n")

    if args.output:
        f.close()
            
if __name__ == "__main__":
    # validate input
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the letters to de-scramble")
    parser.add_argument("-d", "--dictionary",
                        help="override the default dictionary file",
                        default="words/voldemot-dict.txt")
    parser.add_argument("-c", "--count",
                        help="number of words to combine (default: 2)",
                        type=int, default=2)
    parser.add_argument("-v", "--verbose",
                        help="show progress", action="store_true")
    parser.add_argument(
        "-p", "--print", help="print results", action="store_true")
    parser.add_argument(
        "-o", "--output", nargs='?', const="voldemot.txt", help="output file")

    para = parser.parse_args()
    main(para)
