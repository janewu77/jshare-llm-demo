import os
from typing import Iterator, Union
import base64
import json
import websockets
from elevenlabs import stream
from websockets.sync.client import connect

from cfg.cfg import eleventlabs_api_key

api_key = eleventlabs_api_key
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # "Bella"
MODEL_ID = 'eleven_monolingual_v1'

voice_settings = {
                "stability": 0.5,
                "similarity_boost": True
            }


def text_chunker(chunks: Iterator[str]) -> Iterator[str]:
    """Used during input streaming to chunk text blocks and set last char to space"""
    splitters = (".", ",", "?", "!", ";", ":", "—", "-", "(", ")", "[", "]", "}", " ")
    buffer = ""
    for text in chunks:
        if buffer.endswith(splitters):
            yield buffer if buffer.endswith(" ") else buffer + " "
            buffer = text
        elif text.startswith(splitters):
            output = buffer + text[0]
            yield output if output.endswith(" ") else output + " "
            buffer = text[1:]
        else:
            buffer += text
    if buffer != "":
        yield buffer + " "


def generate_stream_input(text: Iterator[str]) -> Iterator[bytes]:
    BOS = json.dumps(
        dict(
            text=" ",
            try_trigger_generation=True,
            voice_settings=voice_settings,
            generation_config=dict(
                chunk_length_schedule=[50],
            ),
        )
    )
    EOS = json.dumps(dict(text=""))

    with connect(
            f"wss://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream-input?model_id={MODEL_ID}",
            additional_headers={
                "xi-api-key": api_key or os.environ.get("ELEVEN_API_KEY")
            },
    ) as websocket:
        # Send beginning of stream
        websocket.send(BOS)

        # Stream text chunks and receive audio
        for text_chunk in text_chunker(text):
            data = dict(text=text_chunk, try_trigger_generation=True)
            websocket.send(json.dumps(data))
            try:
                data = json.loads(websocket.recv(1e-4))
                if data["audio"]:
                    yield base64.b64decode(data["audio"])  # type: ignore
            except TimeoutError:
                pass

        # Send end of stream
        websocket.send(EOS)

        # Receive remaining audio
        while True:
            try:
                data = json.loads(websocket.recv())
                if data["audio"]:
                    yield base64.b64decode(data["audio"])  # type: ignore
            except websockets.exceptions.ConnectionClosed:
                break


def do_generate(text: Union[str, Iterator[str]]) -> Union[bytes, Iterator[bytes]]:
    return generate_stream_input(text)


def text_stream():
    yield "Hi there, I'm Eleven "
    yield "I'm a text to speech API "
    yield "Could"
    yield " you"
    yield " say"
    yield " hi"
    yield " "


audio_stream = do_generate(text=text_stream())
stream(audio_stream)
