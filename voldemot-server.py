"""
Creates a websocket server that listens for a voldemot request
and returns a list of possible word combinations.
"""

import sys
import asyncio
import json
import websockets
import voldemot

def main(args):
    """ voldemot web server """
    asyncio.get_event_loop().run_until_complete(
        websockets.serve(handler, '0.0.0.0', int(args[1])))
    asyncio.get_event_loop().run_forever()

async def send_response(websocket, inputLetters, data):
    """ returns state event in JSON """
    response = json.dumps({'total-matches': str(len(data)), 'letters': inputLetters})
    # print(response)
    await asyncio.wait([websocket.send(response)])
    for index, entry in enumerate(data, 1):
        response = json.dumps({'match': index, 'value':entry})
        await asyncio.wait([websocket.send(response)])

async def handler(websocket, path):
    """ register(websocket) sends user_event() to websocket """
    # await register(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            await handle_message(websocket, data)
    finally:
        # await unregister(websocket)
        pass

async def handle_message(websocket, data):
    """ handles incoming message from players """
    if data['type'] == 'voldemot-request':
        letters = data['input']
        wordsRequested = int(data['word-count'])
        print("Received request for *" + letters + "*, with up to "
              + str(wordsRequested) + "-word combinations")
        inputLetters, matches = voldemot.voldemot(letters, wordsRequested)
        # for entry in matches:
            # print(entry)
        await send_response(websocket, inputLetters, matches)

if __name__ == "__main__":
    main(sys.argv)

