import wave
import json
from tornado import gen
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.websocket import websocket_connect

async def main():
 
    # get a connection
    conn = await websocket_connect('ws://localhost:8080/websocket/')
    print('connection established')

    # open the wav file
    f = wave.open('resources/hello-world.wav', 'rb')

    # create an index
    i = 0

    # read a frame
    frames = f.readframes(320)
    
    # iterate until all frames are used
    while(len(frames) == 640):
 
        # write the frame 
        conn.write_message(frames, binary=True)
        
        # wait for a response
        resp = await conn.read_message()

        # break if the server is closing the connection
        if resp is None:
            break

        # process the response
        rsp = json.loads(resp)

        # check if there is a start index indicator
        if 'startindex' in rsp:
            startindex = rsp['startindex']

        # check the more data indicator
        if 'moredata' in rsp and not rsp['moredata']:
            stopindex = rsp['stopindex']
            print('Server doesn\'t require further data')
            break
    
        # increment a counter and get more frames
        i = i + 1
        frames = f.readframes(320)

    f.close()
    conn.close()

    print('Speech started at frame index: {} time: {}ms and finished at frame index: {} time: {}ms'.format(startindex, startindex * 20, stopindex, stopindex * 20))

IOLoop.current().run_sync(main)
