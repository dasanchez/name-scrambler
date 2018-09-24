"""
voldemor-server
Creates a websocket server that listens for a voldemot request
and returns a list of possible word combinations.
"""

import sys
import asyncio
import json
import re
import websockets
from itertools import product
import voldemot_utils as vol
import wordDB

pauseInterval = 10000
pauseLength = 0.05
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
    global pauseInterval
    global pauseLength

    USERS.add(websocket)
    # pauseInterval -= 5000
    pauseLength += 0.05
    print(f"{len(USERS)} users connected, {pauseLength}ms pause every {pauseInterval} checks")
    await notify_users()

async def unregister(websocket):
    global pauseInterval
    global pauseLength

    USERS.remove(websocket)
    # pauseInterval += 5000
    pauseLength -= 0.05
    print(f"{len(USERS)} users connected, {pauseLength}ms pause every {pauseInterval} checks")
    await notify_users()

def users_event():
    return json.dumps({'type': 'users', 'count': len(USERS)})

async def notify_users():
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def handler(websocket, path):
    """ register(websocket) sends user_event() to websocket """
    await register(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            print("Received data: " + str(data))
            fullMatch = await handle_message(websocket, data)
            response = json.dumps({'total-matches': True, 'value': len(fullMatch)})
            print(response)
            await websocket.send(response)
    finally:
        await unregister(websocket)
        # pass

async def handle_message(websocket, data):
    """ handles incoming message from players """
    if data['type'] == 'voldemot-request':
        letters = data['input']
        wordCount = int(data['word-count'])
        print("Received request for *" + letters + "*, with up to "
              + str(wordCount) + "-word combinations.")

        # START VOLDEMOT ROUTINE
        worddb = wordDB.wordDB()
        worddb.query("CREATE TABLE words(word text, length int)")

        # remove spaces and non-alphabetical characters
        letters = re.sub(r"\W?\d?", "", letters).lower()
        letters = letters[:16]
        sortedLetters = sorted(list(letters))
        wordsFound = vol.findWords("words/voldemot-dict.txt", str(letters), worddb)
        print("Found " + str(len(wordsFound)) + " words.")

        # generate combinations
        lenCombos = vol.splitOptions(len(letters), wordCount)
        print(lenCombos)
        setList = vol.genSetList(lenCombos, worddb)
        setCount = len(setList)

        if setList:
            print("setList length: " + str(setCount))
            if setCount == 1:
                print(setList[0])

        fullMatch = []
        lock = asyncio.Lock()
        progress = [1, setCount]

        for entry in setList:
            await processClientSet(sortedLetters, entry,
                                       lock, fullMatch, progress, websocket)

        # await asyncio.sleep(1)
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
        sortedCombo = sorted(combo)
        letterList = sorted([letter for word in combo for letter in word])
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
        # print(f"Progress: {percent:3}%")
        response = json.dumps({'percent': True, 'value': percent})
        await ws.send(response)
        progress[0] += 1


if __name__ == "__main__":
    main(sys.argv)
