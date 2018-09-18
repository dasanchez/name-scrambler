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
import voldemot_utils as vol
import wordDB

def main(args):
    """ voldemot web server """
    port = int(args[1])
    print(f"Opening websocket server on port {port}...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        websockets.serve(handler, '0.0.0.0', int(args[1])))
    loop.run_forever()

async def handler(websocket, path):
    """ register(websocket) sends user_event() to websocket """
    try:
        async for message in websocket:
            data = json.loads(message)
            print("Received data: " + str(data))
            fullMatch = await handle_message(websocket, data)
            response = json.dumps({'total-matches': True, 'value': len(fullMatch)})
            print(response)
            await websocket.send(response)
    finally:
        pass

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
            await asyncio.sleep(0.25)

            asyncio.ensure_future(vol.processClientSet(sortedLetters, entry,
                                                       lock, fullMatch, progress, websocket))

        await asyncio.sleep(0.5)
        return fullMatch

if __name__ == "__main__":
    main(sys.argv)
