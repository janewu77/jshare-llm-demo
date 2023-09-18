import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

from datetime import datetime
from dateutil import rrule

start_time = datetime.now()

# model_id = "stabilityai/stable-diffusion-2-1"
model_id = "/Users/jingwu/janewu/llm-model/sd/stable-diffusion-2-1"

# Use the DPMSolverMultistepScheduler (DPM-Solver++) scheduler here instead
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
# pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16) # black
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
# pipe = pipe.to("cuda")
pipe = pipe.to("mps")

# Recommended if your computer has < 64 GB of RAM
# pipe.enable_attention_slicing()

# prompt = "a photo of an astronaut riding a horse on mars"
prompt = "a lovely cat, yellow, cute"


image = pipe(prompt).images[0]
image.save("cat.png")

seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
print(f"spend: {seconds.count()} seconds")

start_time = datetime.now()
prompt = "a lovely dog, yellow, cute"
image = pipe(prompt).images[0]
image.save("4.png")

seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
print(f"total spend: {seconds.count()} seconds")
print('【END】.')
