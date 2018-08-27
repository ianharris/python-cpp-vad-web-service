# Overview

This repo creates a Dockerised flask service that will perform Voice Activity Detection (VAD). The service exposes a websocket endpoint. A client can connect to the websocket listener and stream packets of audio. 

While the service requires further frames of audio to analyse it will include a "moredata" key in the JSON response with a value of true.

When the start of speech is detected the service will include a "startindex" key in the JSON response with a value of the index of the last frame submitted.

When the end of speech is detected the service will include a "moredata" key in the JSON response with a value of false. A key of stopindex will also be included with a value of the last frame index submitted.

# Assumptions

A single websocket connection corresponds to a single sample of voice. That is, a connection is opened, voice is streamed until the server indicates no more data is required and then the connection is closed. The connection can't be reused for other voice currently - or certainly isn't intended to be.

# Building and launching

To build the Docker image run the following:

```sh
docker build -t vad .
```

To launch the container run:

```sh
docker run -d -p 8080:8080 vad
```

# Testing

A single test script is included in the repo - 'test.py'. The test script will open the WAV file 'hello-world.wav' included in the 'resources' directory, connect to the websocket end-point and start streaming. When the server indicates that no further data is required it will return a "moredata" false in the response indicating that the client doesn't need to send any more data. The script can be run by running:

```sh
python test.py
```

# TODO

* Further testing should be built out
* Inclusion of meta data (e.g. frame index, has voice started) should be included in the client requests / server responses to remove state from the server; this would have the added benefit of not requiring the assumption that a single web socket connection corresponds to a single sample of voice.

