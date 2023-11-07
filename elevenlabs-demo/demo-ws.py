from elevenlabs import generate, stream, set_api_key

from cfg.cfg import eleventlabs_api_key

set_api_key(eleventlabs_api_key)


def text_stream():
    yield "Hi there, I'm Eleven "
    yield "I'm a text to speech API "
    yield "Could"
    yield " you"
    yield " say"
    yield " hi"
    yield " "


audio_stream = generate(
    text=text_stream(),
    voice="Nicole",
    model="eleven_monolingual_v1",
    stream=True
)
# print(audio_stream)
stream(audio_stream)
