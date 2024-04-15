import torch
from TTS.api import TTS
from datetime import datetime
from dateutil import rrule

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

    def do_tts(self, text, voice, output_file, lang):
        start_time = datetime.now()
        # Run TTS
        # ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
        # Text to speech list of amplitude values as output
        # wav = tts.tts(text="Hello world!", speaker_wav="my/cloning/audio.wav", language="en")
        # Text to speech to a file
        # lang = "zh-cn"
        speaker_wav = f"{self.model_path}/samples/{lang}_sample.wav"
        filepath = self.tts.tts_to_file(text=text, speaker_wav=speaker_wav, language=lang, file_path=output_file)

        seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
        print(f"total spend: {seconds.count()} seconds")

        return filepath


if __name__ == '__main__':
    my_tts = MyCoquiTTSLocal()
    # prompt_txt = '''
    # 我是在线客服，由公司的开发团队开发。 很抱歉，我无法提供开发者的联系方式。
    # '''  # 13s
    lang = "en"
    output_file = f"output_{lang}.wav"
    prompt_txt = '''
    We introduce OpenVoice, a versatile instant voice cloning approach that requires only a short audio clip from the reference speaker to replicate their voice and generate speech in multiple languages.
    '''
    my_tts.do_tts(prompt_txt, "", output_file, lang)


