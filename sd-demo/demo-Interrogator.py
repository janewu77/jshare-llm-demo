import torch
from PIL import Image
from clip_interrogator import Config, Interrogator
from datetime import datetime
from dateutil import rrule

# pip install clip-interrogator==0.6.0
start_time = datetime.now()

# image_path = 'imgs/cat.png'
image_path = '/Users/jingwu/Downloads/before/3861693660109_.pic.jpg'

image = Image.open(image_path).convert('RGB')


# ViT-L-14/openai  Diffusion 1.X
# ViT-H-14/laion2b_s32b_b79k For Stable Diffusion 2.0

# The Config object lets you configure CLIP Interrogator's processing.
#
# clip_model_name: which of the OpenCLIP pretrained CLIP models to use
# cache_path: path where to save precomputed text embeddings
# download_cache: when True will download the precomputed embeddings from huggingface
# chunk_size: batch size for CLIP, use smaller for lower VRAM
# quiet: when True no progress bars or text output will be displayed

if torch.backends.mps.is_available():
    print("mps")


ci = Interrogator(Config(clip_model_name="ViT-L-14/openai", device="mps"))
print(ci.interrogate(image))

# ci = Interrogator(Config(clip_model_name="ViT-H-14/laion2b_s32b_b79k", device="mps"))
# print(ci.interrogate(image))


seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
print(f"total spend: {seconds.count()} seconds")
print('【END】.')