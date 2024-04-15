import torch
from TTS.api import TTS
from datetime import datetime
from dateutil import rrule

import os

'''
# model on local
'''

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"


class MyCoquiTTSLocal:

    tts = None
    model_path = "/Users/jingwu/janewu/llm-model/coqui/XTTS-v2"

    def __init__(self):
        # List available 🐸TTS models
        # print(TTS().list_models())

        # Init TTS
        self.tts = TTS(model_path=self.model_path, config_path=f"{self.model_path}/config.json").to(device)
        # tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    def _do_coqui_tts(self, text, voice, output_file, lang):
        start_time = datetime.now()
        # Run TTS
        # ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
        # Text to speech list of amplitude values as output
        # wav = tts.tts(text="Hello world!", speaker_wav="my/cloning/audio.wav", language="en")
        # Text to speech to a file
        # lang = "zh-cn"
        speaker_wav = f"{self.model_path}/samples/{voice}_sample.wav"
        filepath = self.tts.tts_to_file(text=text, speaker_wav=speaker_wav, language=lang, file_path=output_file)

        seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
        print(f"total spend: {seconds.count()} seconds")

        return filepath

    def do_tts(self, text, voice, output_file, lang="en"):
        output_file_wav = output_file.replace("mp3", "wav")
        self._do_coqui_tts(text, voice, output_file_wav, lang)
        self._wav_2_mp3(output_file_wav, output_file)
        return output_file

    def _wav_2_mp3(self, wav_file, mp3_file):
        from pydub import AudioSegment
        # 读取WAV文件
        wav_audio = AudioSegment.from_file(wav_file, format="wav")

        # 转换为MP3
        wav_audio.export(mp3_file, format="mp3")

        os.remove(wav_file)


if __name__ == '__main__':
    my_tts = MyCoquiTTSLocal()
    # prompt_txt = '''
    # 我是在线客服，由公司的开发团队开发。 很抱歉，我无法提供开发者的联系方式。
    # '''  # 13s
    # lang = "en"

    # prompt_txt = '''
    # We introduce OpenVoice, a versatile instant voice cloning approach that requires only a short audio clip from the reference speaker to replicate their voice and generate speech in multiple languages.
    # '''  # 24s
    prompt_txt = '''
          It's important for you to know that regardless of what you're going through, your worth as a person is not determined by whether or not someone loves you. 
          It sounds like there may be some deeper issues at play here. 
          Have you noticed any patterns in your relationships that make it difficult to feel loved? 
          How do these patterns impact the way you view yourself and others around you?
          '''  # 39s

    for voice in ["en", "LJ025-0076", "jane_2"]:
        output_file = f"../output/demo_coqui_tts_{voice}.mp3"
        output_file = my_tts.do_tts(prompt_txt, voice, output_file)  # asyncio.run()
        from tts.util.sound_util import play_sound
        play_sound(output_file)


