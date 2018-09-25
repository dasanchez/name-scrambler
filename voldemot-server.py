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
    """ new websocket client has connected """
    global pauseInterval
    global pauseLength

    USERS.add(websocket)
    pauseLength += 0.025
    print(f"{len(USERS)} users connected, {pauseLength:.2f}ms pause every {pauseInterval} checks")
    await notify_users()

async def unregister(websocket):
    """ websocket client has disconnected """
    global pauseInterval
    global pauseLength

    USERS.remove(websocket)
    pauseLength -= 0.025
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

async def handler(websocket, path):
    """ register(websocket) sends user_event() to websocket """
    await register(websocket)
    try:
        async for message in websocket:
            start = time.time()
            data = json.loads(message)
            fullMatch = await handle_message(websocket, data)
            response = json.dumps({'total-matches': True, 'value': len(fullMatch)})
            print(response)
            await websocket.send(response)
            await asyncio.sleep(0.5)
            end = time.time()
            print(f"Processed request in {(end-start):.2f} seconds")
            return 'done'
    finally:
        await unregister(websocket)
        # pass

async def handle_message(websocket, data):
    """ handles incoming message from players """
    if data['type'] == 'voldemot-request':
        letters = data['input']
        wordCount = int(data['word-count'])

        # START VOLDEMOT ROUTINE
        worddb = wordDB.wordDB()
        worddb.query("CREATE TABLE words(word text, length int)")

        # remove spaces and non-alphabetical characters
        letters = re.sub(r"\W?\d?", "", letters).lower()
        letters = letters[:16]
        print(f"Processing {letters} for {wordCount}-word combinations.")
        sortedLetters = sorted(list(letters))
        wordsFound = vol.findWords("words/voldemot-dict.txt", str(letters), worddb)
        print("Found " + str(len(wordsFound)) + " words.")

        # generate combinations
        lenCombos = vol.splitOptions(len(letters), wordCount)
        setList = vol.generateCandidates(lenCombos, worddb)
        setCount = len(setList)

        if setList:
            print(f"{setCount} combination sets:")
            print(lenCombos)

        fullMatch = []
        lock = asyncio.Lock()
        progress = [1, setCount]

        for entry in setList:
            await processClientSet(sortedLetters, entry,
                                   lock, fullMatch, progress, websocket)

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
