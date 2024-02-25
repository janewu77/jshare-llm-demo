from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# 需要至少100G+内存
device = "mps"
model_id = "/Users/jingwu/janewu/llm-model/mistralai/Mixtral-8x7B-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_id)

# model = AutoModelForCausalLM.from_pretrained(model_id)

# Lower precision using (8-bit & 4-bit) using bitsandbytes
# model = AutoModelForCausalLM.from_pretrained(model_id, load_in_4bit=True)

# In half-precision（100G+）
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16).to(device)

# Load the model with Flash Attention 2
# model = AutoModelForCausalLM.from_pretrained(model_id, use_flash_attention_2=True)
# model.to(device)

text = "Hello my name is"
# inputs = tokenizer(text, return_tensors="pt")
inputs = tokenizer(text, return_tensors="pt").to(device)

outputs = model.generate(**inputs, max_new_tokens=20)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))



