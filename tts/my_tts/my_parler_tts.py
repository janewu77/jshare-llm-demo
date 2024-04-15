import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf

from datetime import datetime
from dateutil import rrule

import os

'''
# 本地跑的模型
'''

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
os.environ['TOKENIZERS_PARALLELISM'] = 'true'


class MyParlerTTSLocal:

    # tts = None
    model_path = "/Users/jingwu/janewu/llm-model/parler-tts/parler_tts_mini_v0.1"
    model = None
    tokenizer = None

    def __init__(self):
        # Init TTS
        start_time = datetime.now()
        self.model = ParlerTTSForConditionalGeneration.from_pretrained(self.model_path).to(device)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
        print(f"init total spend: {seconds.count()} seconds")

    def _do_coqui_tts(self, prompt, output_file_name, description):
        start_time = datetime.now()

        # prompt = "Hey, how are you doing today?"
        # description = "A male speaker with a slightly low-pitched voice delivers his words quite expressively, in a very confined sounding environment with clear audio quality. He speaks very fast."

        input_ids = self.tokenizer(description, return_tensors="pt").input_ids.to(device)
        prompt_input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids.to(device)

        generation = self.model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
        audio_arr = generation.cpu().numpy().squeeze()
        sf.write(output_file_name, audio_arr, self.model.config.sampling_rate)

        seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
        print(f"generate3 total spend: {seconds.count()} seconds")
        return output_file_name

    def do_tts(self, text, voice, output_file, lang="en", description=""):
        output_file_wav = output_file
        output_file_wav = output_file_wav.replace("mp3", "wav")
        self._do_coqui_tts(text, output_file_wav, description)
        MyParlerTTSLocal._wav_2_mp3(output_file_wav, output_file)
        return output_file

    @staticmethod
    def _wav_2_mp3(wav_file, mp3_file):
        from pydub import AudioSegment
        # 读取WAV文件
        wav_audio = AudioSegment.from_file(wav_file, format="wav")

        # 转换为MP3
        wav_audio.export(mp3_file, format="mp3")
        # os.remove(wav_file)


if __name__ == '__main__':
    my_tts = MyParlerTTSLocal()

    # prompt_txt = '''
    # We introduce OpenVoice, a versatile instant voice cloning approach that requires only a short audio clip from the reference speaker to replicate their voice and generate speech in multiple languages.
    # '''  # 24s
    # # Have you noticed any patterns in your relationships that make it difficult to feel loved?
    # prompt_txt = "Hey, how are you doing today?"
    prompt_txt = '''
        How do these patterns impact the way you view yourself and others around you?   
    '''

    voice_desc_male = "A male speaker with a slightly low-pitched voice delivers his words quite expressively, in a very confined sounding environment with clear audio quality. He speaks very fast."
    voice_desc_female = "A female speaker with a slightly low-pitched voice delivers her words quite expressively, in a very confined sounding environment with clear audio quality. She speaks very fast."
    voice_desc_baby = " a male speak. he speaks very slow"
    for voice_desc in ["voice_desc_male", "voice_desc_female", "voice_desc_baby"]:
        output_file = f"../output/demo_parlet_tts_{voice_desc}.mp3"
        output_file2 = my_tts.do_tts(prompt_txt, "", output_file, "", voice_desc)
        from tts.util.sound_util import play_sound
        play_sound(output_file2)


