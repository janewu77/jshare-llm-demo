
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# 官言模型，从hf下载
model_path = "/Users/jingwu/janewu/llm-model/gemma/gemma-7b-it"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto", torch_dtype=torch.float16)
# , torch_dtype=torch.float16

input_text = "Write me a poem about Machine Learning."
input_ids = tokenizer(input_text, return_tensors="pt").to("mps")

outputs = model.generate(**input_ids)
print(tokenizer.decode(outputs[0]))
