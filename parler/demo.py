import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf

from datetime import datetime
from dateutil import rrule

start_time = datetime.now()
device = "cuda:0" if torch.cuda.is_available() else "cpu"

model_path = "/Users/jingwu/janewu/llm-model/parler-tts/parler_tts_mini_v0.1"
model = ParlerTTSForConditionalGeneration.from_pretrained(model_path).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_path)

prompt = "Hey, how are you doing today?"
description = "A male speaker with a slightly low-pitched voice delivers his words quite expressively, in a very confined sounding environment with clear audio quality. He speaks very fast."
# 17s

input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
prompt_input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
audio_arr = generation.cpu().numpy().squeeze()
sf.write("parler_tts_out.wav", audio_arr, model.config.sampling_rate)

seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
print(f"total spend: {seconds.count()} seconds")
# play_sound(output_file)
