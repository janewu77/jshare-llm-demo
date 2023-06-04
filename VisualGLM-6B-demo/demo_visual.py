import torch
from transformers import AutoTokenizer, AutoModel
from dateutil import rrule
from datetime import datetime

# chatglm_path = '/Users/janewu/llm-model/visualglm-6b'
chatglm_path = '/Users/jingwu/janewu/llm-model/20230603/visualglm-6b'
DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
print(f"DEVICE:{DEVICE}")

tokenizer = AutoTokenizer.from_pretrained(chatglm_path, trust_remote_code=True, revision="v1.1.0")
model = AutoModel.from_pretrained(chatglm_path, trust_remote_code=True, revision="v1.1.0").half().to(DEVICE)
# model = model.eval()

my_now = datetime.now()
image_path = "imgs/coffee.pic.jpg"
response, history = model.chat(tokenizer, image_path, "描述这张图片。", history=[], temperature=0.8)
print(response)
print(f"[total spend]: {rrule.rrule(freq=rrule.SECONDLY, dtstart=my_now, until=datetime.now()).count()} seconds")

response, history = model.chat(tokenizer, image_path, "这张图片可能是在什么场所拍摄的？", history=history, temperature=0.8)
print(response)
print(f"[total spend]: {rrule.rrule(freq=rrule.SECONDLY, dtstart=my_now, until=datetime.now()).count()} seconds")

print("=====================")
image_path = "imgs/1.jpg"
response, history = model.chat(tokenizer, image_path, "", history=[], temperature=0.8)
print(response)
print(f"[total spend]: {rrule.rrule(freq=rrule.SECONDLY, dtstart=my_now, until=datetime.now()).count()} seconds")

response, history = model.chat(tokenizer, image_path, "这张图片可能是在什么场所拍摄的？", history=history, temperature=0.8)
print(response)
print(f"[total spend]: {rrule.rrule(freq=rrule.SECONDLY, dtstart=my_now, until=datetime.now()).count()} seconds")


