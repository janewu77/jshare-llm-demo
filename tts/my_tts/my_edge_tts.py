import asyncio
import edge_tts
from datetime import datetime
from dateutil import rrule

"""
#  use Microsoft Edge's online text-to-speech service 
# 微软的edge_tts在线服务 
# install
# $ pip install edge-tts
- 非常好用的一个tts。
- 需要网络, 没有费用产生，不需要api key
- 速度非常快
- Changing the voice
- 不支持Custom SSML
- Changing rate, volume and pitch
"""


class MyEdgeTTS:

    @classmethod
    async def do_tts(cls, text, voice, output_file) -> None:
        """Main function"""
        # voices = await VoicesManager.create()
        # voice = voices.find(Gender="Male", Language="es")
        # print(voice)
        # Also supports Locales
        # voice = voices.find(Gender="Female", Locale="es-AR")

        # communicate = my_edge_tts.Communicate(TEXT, random.choice(voice)["Name"])
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        return output_file

    @classmethod
    def do_tts_one(cls, text, voice, output_file):
        start_time = datetime.now()

        loop = asyncio.get_event_loop_policy().get_event_loop()
        try:
            loop.run_until_complete(cls.do_tts(text, voice, output_file))
        finally:
            loop.close()

        seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
        print(f"total spend: {seconds.count()} seconds")


if __name__ == "__main__":
    import asyncio
    VOICE = 'en-US-SteffanNeural' # en-US-SteffanNeural en-US-MichelleNeural
    OUTPUT_FILE = f"../output/demo_edge_{VOICE}.mp3"
    # TEXT = '''
    # We introduce OpenVoice, a versatile instant voice cloning approach
    # that requires only a short audio clip from the reference speaker to replicate
    # their voice and generate speech in multiple languages.
    # '''
    TEXT = '''
        It's important for you to know that regardless of what you're going through, your worth as a person is not determined by whether or not someone loves you. 
        It sounds like there may be some deeper issues at play here. 
        Have you noticed any patterns in your relationships that make it difficult to feel loved? 
        How do these patterns impact the way you view yourself and others around you?
        '''  # 39s
    start_time = datetime.now()
    output_file = asyncio.run(MyEdgeTTS.do_tts(TEXT, VOICE, OUTPUT_FILE))
    # output_file = MyEdgeTTS.do_tts(TEXT, VOICE, OUTPUT_FILE)
    seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
    print(f"total spend: {seconds.count()} seconds")

    from tts.util.sound_util import play_sound
    play_sound(output_file)

