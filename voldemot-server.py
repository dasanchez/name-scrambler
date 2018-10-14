"""
voldemor-server
Creates a websocket server that listens for a voldemot request
and returns a list of possible word combinations.
"""

import sys
import asyncio
import json
import re
import time
from itertools import product
import websockets
import voldemot_utils as vol

pauseInterval = 10000
pauseLength = 0.04
USERS = set()

def main(args):
    """ voldemot web server """
    port = int(args[1])
    print(f"Opening websocket server on port {port}...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        websockets.serve(handler, '0.0.0.0', int(args[1])))
    loop.run_forever()

async def register(websocket):
    """ new websocket client has connected """
    global pauseLength

    USERS.add(websocket)
    pauseLength += 0.01
    print(f"{len(USERS)} users connected, {pauseLength:.2f}ms pause every {pauseInterval} checks")
    await notify_users()

async def unregister(websocket):
    """ websocket client has disconnected """
    global pauseLength

    USERS.remove(websocket)
    pauseLength -= 0.01
    print(f"{len(USERS)} users connected, {pauseLength:.2f}ms pause every {pauseInterval} checks")
    await notify_users()

def users_event():
    """ generate message for user notification """
    return json.dumps({'type': 'users', 'count': len(USERS)})

async def notify_users():
    """ notify clients of a change in users connected """
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def reject_connection(websocket):
    message = json.dumps({'reject': True, 'reason': 'max-users'})
    await websocket.send(message)

async def handler(websocket, path):
    """ register(websocket) sends user_event() to websocket """
    if len(USERS) >= 5:
        await reject_connection(websocket)
        print("Rejected new connection")
        return
    else:
        await register(websocket)
        try:
            async for message in websocket:
                start = time.time()
                data = json.loads(message)
                fullMatch = await handle_message(websocket, data)
                response = json.dumps({'total-matches': True, 'value': len(fullMatch)})
                await websocket.send(response)
                await asyncio.sleep(0.5)
                
                end = time.time()
                print(f"Processed request for {data['input']} in {(end-start):.2f} seconds," +
                      f"generating {len(fullMatch)} combinations.")
                return 'done'
        finally:
            await unregister(websocket)

async def twoWordCombinations(wordsFound, letters, websocket):
    """ return a list of two-word combinations """
    global pauseInterval
    global pauseLength
    pause = pauseInterval
    
    fullMatch = []
    firstList = wordsFound.copy()
    total = 0
    percent = 0
    rootList = vol.getWordsUnder(firstList, len(letters) - 1)
    for first in rootList:
        total += 1
        secondList = firstList.copy()
        for second in vol.getWordsEqualTo(secondList, len(letters) - len(first)):
            testCombo = first + second
            if sorted(testCombo) == sorted(letters):
                testComboStr = str(f"{first} {second}")
                fullMatch.append(testComboStr)
                response = json.dumps({'match': True, 'value': testComboStr})
                await websocket.send(response)
            
            pause -= 1
            if pause == 0:
                await asyncio.sleep(pauseLength)
                pause = pauseInterval

        firstList.remove(first)
        newPercent = int(total * 100 / len(rootList))
        if newPercent != percent:
            percent = newPercent
            response = json.dumps({'percent': True, 'value': percent})
            await websocket.send(response)
    return fullMatch

async def threeWordCombinations(wordsFound, letters, websocket):
    """ return a list of three-word combinations """
    global pauseInterval
    global pauseLength
    pause = pauseInterval
    
    fullMatch = []
    firstList = wordsFound.copy()
    total = 0
    percent = 0
    rootList = vol.getWordsUnder(firstList, len(letters) - 2)
    for first in rootList:
        total += 1
        secondList = firstList.copy()
        for second in vol.getWordsUnder(secondList, len(letters) - len(first)):
            twoWordCombo = first + second
            if vol.wordIsPresent(twoWordCombo, letters):
                thirdList = secondList.copy()
                for third in vol.getWordsEqualTo(thirdList, len(letters) - len(twoWordCombo)):
                    testCombo = twoWordCombo + third
                    if sorted(testCombo) == sorted(letters):
                        testComboStr = str(f"{first} {second} {third}")
                        fullMatch.append(testComboStr)
                        response = json.dumps({'match': True, 'value': testComboStr})
                        await websocket.send(response)
                    
                    pause -= 1
                    if pause == 0:
                        await asyncio.sleep(pauseLength)
                        pause = pauseInterval

            secondList.remove(second)
        firstList.remove(first)
        newPercent = int(total * 100 / len(rootList))
        if newPercent != percent:
            percent = newPercent
            response = json.dumps({'percent': True, 'value': percent})
            await websocket.send(response)
    return fullMatch

async def fourWordCombinations(wordsFound, letters, websocket):
    """ return a list of four-word combinations """
    global pauseInterval
    global pauseLength
    pause = pauseInterval

    fullMatch = []
    total = 0
    percent = 0
    firstList = wordsFound.copy()
    rootList = vol.getWordsUnder(firstList, len(letters) - 3)
    for first in rootList:
        total += 1
        secondList = firstList.copy()
        for second in vol.getWordsUnder(secondList, len(letters) - len(first) - 2):
            twoWordCombo = first + second
            if vol.wordIsPresent(twoWordCombo, letters):
                thirdList = secondList.copy()
                for third in vol.getWordsUnder(thirdList, len(letters) - len(twoWordCombo)):
                    threeWordCombo = twoWordCombo + third
                    if vol.wordIsPresent(threeWordCombo, letters):
                        fourthList = thirdList.copy()
                        for fourth in vol.getWordsEqualTo(fourthList, len(letters) - len(threeWordCombo)):
                            fourWordCombo = threeWordCombo + fourth
                            if sorted(fourWordCombo) == sorted(letters):
                                testComboStr = f"{first} {second} {third} {fourth}"
                                fullMatch.append(testComboStr)
                                response = json.dumps({'match': True, 'value': testComboStr})
                                await websocket.send(response)

                            pause -= 1
                            if pause == 0:
                                await asyncio.sleep(pauseLength)
                                pause = pauseInterval

                    thirdList.remove(third)
            secondList.remove(second)
        firstList.remove(first)
        newPercent = int(total * 100 / len(rootList))
        if newPercent != percent:
            percent = newPercent
            response = json.dumps({'percent': True, 'value': percent})
            await websocket.send(response)
    return fullMatch


async def findWordCombinations(wordsFound, letters, wordCount, websocket):
    ''' find 2+ word combinations '''
    global pauseInterval
    global pauseLength
    pause = pauseInterval
    
    fullMatch = []
    rootList = vol.getWordsUnder(wordsFound, len(letters) - (wordCount - 2))
    tempWords = rootList.copy()
    lettersLength = len(letters)

    total = 0
    percent = 0

    for root in rootList:
        # traverse the remainder of the list until it's all gone
        total += 1
        prefixList = [root]
        for baggageCounter in range(2, wordCount+1):
            newPrefixList = []
            for prefix in prefixList:
                lastPrefix = prefix.split(' ')[-1]
                tempList = tempWords[tempWords.index(lastPrefix):]
                collapsedPrefix = prefix.replace(" ", "")
                spotsAvailable = lettersLength - len(collapsedPrefix)

                if baggageCounter == wordCount:
                    for tempWord in vol.getWordsEqualTo(tempList, spotsAvailable):
                        if sorted(collapsedPrefix + tempWord) == sorted(letters):
                            newMatch = f"{prefix} {tempWord}"
                            fullMatch.append(newMatch)
                            if websocket:
                                response = json.dumps({'match': True, 'value': newMatch})
                                await (websocket.send(response))
                else:
                    baggageLeft = spotsAvailable - (wordCount - baggageCounter - 1)
                    for tempWord in vol.getWordsUnder(tempList, baggageLeft):
                        if vol.wordIsPresent(collapsedPrefix + tempWord, letters):
                            newPrefixList.append(f"{prefix} {tempWord}")

                pause -= 1
                if pause == 0:
                    await asyncio.sleep(pauseLength)
                    pause = pauseInterval
            prefixList = newPrefixList.copy()

        tempWords.remove(root)
        newPercent = int(total * 100 / len(rootList))
        if newPercent != percent:
            percent = newPercent
            response = json.dumps({'percent': True, 'value': percent})
            await websocket.send(response)

    return fullMatch


async def handle_message(websocket, data):
    """ handles incoming message from players """
    if data['type'] == 'voldemot-request':
        letters = data['input']
        wordCount = int(data['word-count'])

        # START VOLDEMOT ROUTINE
        # Remove spaces and non-alphabetical characters
        letters = re.sub(r"\W?\d?", "", letters).lower()
        letters = letters[:16]
        print(f"Processing {letters} for {wordCount}-word combinations.")

        response = json.dumps({'input': True, 'value': letters})
        await websocket.send(response)

        sortedLetters = sorted(list(letters))
        wordsFound = vol.getWordList("words/voldemot-dict.txt", str(letters))
        print("Found " + str(len(wordsFound)) + " words.")

        for word in wordsFound:
            response = json.dumps({'rootWord': True, 'value': word})
            await websocket.send(response)

        if wordCount == 1:
            fullMatch = []
            total = 0
            percent = 0
            rootList = vol.getWordsEqualTo(wordsFound, len(letters))
            for word in rootList:
                total += 1
                if sorted(word) == sortedLetters:
                    response = json.dumps({'match': True, 'value': word})
                    await websocket.send(response)
                    fullMatch.append(word)
                newPercent = int(total * 100 / len(rootList))
                if newPercent != percent:
                    percent = newPercent
                    response = json.dumps({'percent': True, 'value': percent})
                    await websocket.send(response)
        else:
            fullMatch = await findWordCombinations(wordsFound, str(letters), wordCount, websocket)
        # elif wordCount == 2:
            # fullMatch = await twoWordCombinations(wordsFound, str(letters), websocket)
        # elif wordCount == 3:
            # fullMatch = await threeWordCombinations(wordsFound, str(letters), websocket)
        # elif wordCount == 4:
            # fullMatch = await fourWordCombinations(wordsFound, str(letters), websocket)

        return fullMatch

async def processClientSet(sortedSoup, wordSet, lock, fullMatch, progress, ws):
    """
    Compares a set of words to the sorted letters and returns all matches.
    """
    global pauseInterval
    global pauseLength

    comboSet = []
    pause = pauseInterval
    for combo in product(*wordSet):
        setEntry = []
        for entry in combo:
            if isinstance(entry, tuple):
                for subset in entry:
                    setEntry.append(subset)
            else:
                setEntry.append(entry)
        sortedCombo = sorted(setEntry)
        letterList = sorted([letter for word in setEntry for letter in word])
        if sortedSoup == letterList and sortedCombo not in comboSet:
            comboSet.append(sortedCombo)
            response = json.dumps({'match': True, 'value': sortedCombo})
            await (ws.send(response))

        pause -= 1
        if pause == 0:
            await asyncio.sleep(pauseLength)
            pause = pauseInterval

    with await lock:
        fullMatch.extend(comboSet)
        percent = int(progress[0]*(100/progress[1]))
        response = json.dumps({'percent': True, 'value': percent})
        await ws.send(response)
        progress[0] += 1

if __name__ == "__main__":
    main(sys.argv)
