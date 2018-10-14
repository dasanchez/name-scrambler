import asyncio
import voldemot_utils as vol

def test_wordPresent():
    assert vol.wordIsPresent('a', 'a') == True
    assert vol.wordIsPresent('art', 'arat') == True
    assert vol.wordIsPresent('art', 'at') == False

def test_getWordsUnder():
    sourceList = ['a', 'ab', 'abc', 'abcd']
    oneList = []
    twoList = ['a']
    threeList = ['a', 'ab']
    fourList = ['a', 'ab', 'abc']
    fiveList = ['a', 'ab', 'abc', 'abcd']

    assert vol.getWordsUnder(sourceList, 1) == oneList
    assert vol.getWordsUnder(sourceList, 2) == twoList
    assert vol.getWordsUnder(sourceList, 3) == threeList
    assert vol.getWordsUnder(sourceList, 4) == fourList
    assert vol.getWordsUnder(sourceList, 5) == fiveList

def test_getWordsEqual():
    sourceList = ['a', 'ab', 'bc', 'ac', 'abc', 'cba', 'abcd']
    zeroList = []
    oneList = ['a']
    twoList = ['ab', 'bc', 'ac']
    threeList = ['abc', 'cba']
    fourList = ['abcd']

    assert vol.getWordsEqualTo(sourceList, 0) == zeroList
    assert vol.getWordsEqualTo(sourceList, 1) == oneList
    assert vol.getWordsEqualTo(sourceList, 2) == twoList
    assert vol.getWordsEqualTo(sourceList, 3) == threeList
    assert vol.getWordsEqualTo(sourceList, 4) == fourList

def test_wordCombinations():
    wordList = ['a', 'age', 'ago', 'an', 'away', 'be', 'bile', 'cab', 'ego', 'even', 'fake', 'gave', 'give', 'given', 'go', 
                'hi', 'hive', 'hoe', 'i', 'in', 'it', 'leg', 'log', 'new', 'newt', 'nile', 'no', 'on', 'oven', 'tin', 'trip', 'way', 'we', 'web', 'well', 'went', 'wet', 'will', 'win', 'won']

    loop = asyncio.get_event_loop()
    resultsList = loop.run_until_complete(vol.findWordCombinations(wordList, 'igo', 2))
    assert resultsList == ['go i']

    resultsList = loop.run_until_complete(vol.findWordCombinations(wordList, 'iwent', 2))
    assert resultsList == ['i newt', 'i went', 'in wet', 'it new', 'tin we']

    resultsList = loop.run_until_complete(vol.findWordCombinations(wordList, 'ihavegone', 3))
    assert resultsList == ['a given hoe', 'age hi oven', 'age hive no', 'age hive on', 'ago even hi', 'an ego hive', 'an give hoe', 'gave hoe in']

    resultsList = loop.run_until_complete(vol.findWordCombinations(wordList, 'wegoaway', 3))
    assert resultsList == ['ago way we', 'away go we']

    resultsList = loop.run_until_complete(vol.findWordCombinations(wordList, 'wewillbegone', 4))
    assert resultsList == ['be ego new will', 'be ego well win', 'bile leg we won', 'bile log new we', 'ego in web well', 'log nile we web']

    resultsList = loop.run_until_complete(vol.findWordCombinations(wordList, 'raipfaetkacb', 4))
    assert resultsList == ['a cab fake trip']

    loop.close()

