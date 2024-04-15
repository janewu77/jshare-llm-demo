from datetime import datetime

from dateutil import rrule
from optimum.bettertransformer import BetterTransformer
from transformers import AutoProcessor, BarkModel
import scipy
import torch
# my_now = datetime.now()

# def get_current_device():
#     # print("get_current_device...")
#
#     DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
#     DEVICE_ID = "0"
#     CUDA_DEVICE = f"{DEVICE}:{DEVICE_ID}" if DEVICE_ID else DEVICE
#     # if debug:
#     print(f"DEVICE:{DEVICE}")
#     return DEVICE, CUDA_DEVICE
#
# DEVICE, CUDA_DEVICE = get_current_device()


device = "cuda" if torch.cuda.is_available() else "cpu"
# device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

# 指定本地模型
model_path = "/Users/jingwu/janewu/llm-model/bark/bark"
processor = AutoProcessor.from_pretrained(model_path)
model = BarkModel.from_pretrained(model_path, torch_dtype=torch.float).to(device)

# convert to bettertransformer
model = BetterTransformer.transform(model, keep_original_model=False)

sample_rate = model.generation_config.sample_rate


def do_tts(voice_preset, text_prompt, output_wave_fn):
    my_now = datetime.now()
    inputs = processor(text_prompt, voice_preset=voice_preset)
    # print(inputs)
    audio_array = model.generate(**inputs)
    audio_array = audio_array.cpu().numpy().squeeze()

    # save them as a .wav file
    scipy.io.wavfile.write(output_wave_fn, rate=sample_rate, data=audio_array)
    print(f"[total spend]: {rrule.rrule(freq=rrule.SECONDLY, dtstart=my_now, until=datetime.now()).count()} seconds")


def do_gen_example():
    # v2/en_speaker_6" v2/en_speaker_0"
    # "v2/en_speaker_0"
    text_prompt = "Hi! Of course, we can talk about snacks. What would you like to discuss?"
    # text_prompt = "我是东圆有线网络有限公司的在线AI客服，由公司的开发团队开发。很抱歉，我无法提供开发者的联系方式。"
    for i in range(10):
        voice_preset = f"v2/en_speaker_{i}"
        output_wave_fn = f"bark_output_{i}.en.wav"
        do_tts(voice_preset, text_prompt, output_wave_fn)


if __name__ == '__main__':
    # do_gen_example()
    # text_prompt = "我是东圆有线网络有限公司的在线AI客服，由公司的开发团队开发。很抱歉，我无法提供开发者的联系方式。"
    # voice_preset = f"v2/zh_speaker_0"
    # output_wave_fn = f"bark_output_0.zh.wav"
    # do_tts(voice_preset, text_prompt, output_wave_fn)

    text_prompt = '''
    The word "excursion" refers to a short journey or trip, especially one taken as a leisure activity. It typically involves going to a different place, often for enjoyment or educational purposes, and returning within a short period, like within a day.
    '''
    voice_preset = f"v2/en_speaker_0"
    do_tts(voice_preset, text_prompt, "output_wave_male.wav")
    voice_preset = f"v2/en_speaker_9"
    do_tts(voice_preset, text_prompt, "output_wave_female.wav")


