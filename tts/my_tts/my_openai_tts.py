import cfg.cfg
from openai import OpenAI
from datetime import datetime
from dateutil import rrule



"""
# openAI的接口，收费的 100
# tts-1 100 RPM ; tts-1-hd 7RPM
# Whisper	$0.006 / minute (rounded to the nearest second)
# TTS	$15.00 / 1M characters
# TTS HD	$30.00 / 1M characters

"""

client = OpenAI()


class MyOPENAITTS:

    def text_to_speech_stream_openai(self, text: str):
        print('Generating audio from text review using Open AI API')
        client = OpenAI()
        # without stream=True is: response: HttpxBinaryResponseContent
        response = client.audio.speech.create(
            model="tts-1",
            voice="echo",
            input=text,
        )  # type: ignore
        chunk_size = 1024
        for data in response.iter_bytes(chunk_size):
            yield data

    @classmethod
    def do_tts(cls, text, voice, output_file):
        response = client.audio.speech.create(
            model="tts-1",  # tts-1 tts-1-hd
            voice=voice,  # alloy, echo, fable, onyx, nova, and shimmer
            input=text,
        )

        response.write_to_file(output_file)
        return output_file


if __name__ == "__main__":
    # text = input("Enter text: ")
    start_time = datetime.now()
    # text = "你好呀，今天天气明媚，你想去哪里玩么？ Today is a wonderful day to build something people love!"
    # text = '''
    #     We introduce OpenVoice, a versatile instant voice cloning approach
    #     that requires only a short audio clip from the reference speaker to replicate
    #     their voice and generate speech in multiple languages.
    #     ''' # 3s
    # text = '''
    #     It's important for you to know that regardless of what you're going through, your worth as a person is not determined by whether or not someone loves you.
    #     It sounds like there may be some deeper issues at play here.
    #     Have you noticed any patterns in your relationships that make it difficult to feel loved?
    #     How do these patterns impact the way you view yourself and others around you?
    #     '''  # 39s
    text = '''How do these patterns impact the way you view yourself and others around you?'''

    # text = '''
    #         Ich liebe dich
    #         '''
    # alloy, echo, fable, onyx, nova, and shimmer
    voice = "shimmer"
    output_file = MyOPENAITTS.do_tts(text, voice, f"../output/demo_openai_tts_{voice}.mp3")
    print(f"output_file:{output_file}")
    seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
    print(f"total spend: {seconds.count()} seconds")
    from tts.util.sound_util import play_sound
    play_sound(output_file)






