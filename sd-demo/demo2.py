
import torch
from diffusers import DiffusionPipeline
from datetime import datetime
from dateutil import rrule

start_time = datetime.now()
model_id = "/Users/jingwu/janewu/llm-model/sd/stable-diffusion-2-1"

pipe = DiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("mps")

# Recommended if your computer has < 64 GB of RAM
pipe.enable_attention_slicing()

prompt = "a lovely dog, yellow, cute"

# # First-time "warmup" pass if PyTorch version is 1.13 (see explanation above)
# _ = pipe(prompt, num_inference_steps=1)

# Results match those from the CPU device after the warmup pass.
image = pipe(prompt).images[0]

image.save("imgs/dog.png")

seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
print(f"total spend: {seconds.count()} seconds")
print('【END】.')

