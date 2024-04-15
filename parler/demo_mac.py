from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf

from datetime import datetime
from dateutil import rrule

import torch


def init(model_path):
    start_time = datetime.now()
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f"device: {device}")
    model = ParlerTTSForConditionalGeneration.from_pretrained(model_path).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
    print(f"init total spend: {seconds.count()} seconds")
    return model, tokenizer, device


def run(model, tokenizer, device, prompt, description, output_file):
    print(f"device: {device}")

    start_time = datetime.now()
    input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
    prompt_input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

    generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
    audio_arr = generation.cpu().numpy().squeeze()
    sf.write(output_file, audio_arr, model.config.sampling_rate)

    seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
    print(f"generation total spend: {seconds.count()} seconds")
    return seconds.count()


def verify_mps_support():
    # The output should show:tensor([1.], device='mps:0')
    if torch.backends.mps.is_available():
        mps_device = torch.device("mps")
        x = torch.ones(1, device=mps_device)
        print(x)
    else:
        print("MPS device not found.")


def init_mps(model_path):
    verify_mps_support()

    start_time = datetime.now()
    device = "mps:0"
    print(f"device: {device}")
    model = ParlerTTSForConditionalGeneration.from_pretrained(model_path).to(device=device, dtype=torch.bfloat16)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
    print(f"init total spend: {seconds.count()} seconds")
    return model, tokenizer, device


def run_mps(model, tokenizer, device, prompt, description, output_file):
    print(f"device: {device}")
    start_time = datetime.now()

    input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
    prompt_input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

    generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
    audio_arr = generation.to(torch.float32).cpu().numpy().squeeze()
    sf.write(output_file, audio_arr, model.config.sampling_rate)

    seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
    print(f"generation total spend: {seconds.count()} seconds")
    return seconds.count()


if __name__ == '__main__':

    model_path = "/Users/jingwu/janewu/llm-model/parler-tts/parler_tts_mini_v0.1"

    # 1s
    prompt_1 = "Hey, how are you doing today?"
    # 3s
    prompt_3 = " How do these patterns impact the way you view yourself and others around you? "
    prompt_7 = " It's important for you to know that regardless of what you're going through, your worth as a person is not determined by whether or not someone loves you.  "
    prompt_9 = "Ever since ChatGPT catapulted generative AI into public consciousness over a year ago, we’ve been introduced to thousands of new consumer products that incorporate the magic of AI — from video generators to workflow hacks, creativity tools to virtual companions."
    prompt_16 = '''The image displays a modern indoor café or break area bathed in natural light, which flows in through a large, curved glass wall offering a view of verdant trees and distant buildings. Inside, there are simple, white round tables paired with understated tan chairs, all arranged neatly within the space.'''

    description = "A male speaker with a slightly low-pitched voice delivers his words quite expressively, in a very confined sounding environment with clear audio quality. He speaks very fast."

    # cpu
    model, tokenizer, devices = init(model_path)
    i = 1
    for prompt in [prompt_1, prompt_3, prompt_7, prompt_9, prompt_16]:
        run(model, tokenizer, devices, prompt, description, f"output_cpu_{i}.wav")
        i = i + 1

    # mps
    model, tokenizer, devices = init_mps(model_path)
    i = 1
    for prompt in [prompt_1, prompt_3, prompt_7, prompt_9, prompt_16]:
        run_mps(model, tokenizer, devices, prompt, description, f"output_mps_{i}.wav")
        i = i + 1


