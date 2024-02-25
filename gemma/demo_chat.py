from transformers import AutoTokenizer, AutoModelForCausalLM
from datetime import datetime
from dateutil import rrule


# 官言模型，从hf下载
# chat 模式
# <bos><start_of_turn>user
# Write a hello world program<end_of_turn>
# <start_of_turn>model

model_id = "/Users/jingwu/janewu/llm-model/gemma/gemma-7b-it"
# dtype = torch.bfloat16

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    # torch_dtype=dtype,
)

chat = [
    {"role": "user", "content": "who are you"},
]


start_time = datetime.now()
prompt = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)

inputs = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
outputs = model.generate(input_ids=inputs.to(model.device), max_new_tokens=250)
print(tokenizer.decode(outputs[0]))
seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
print(f"total spend: {seconds.count()} seconds")




