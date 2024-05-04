import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
from datetime import datetime
from dateutil import rrule

# 使用AutoClass加载
# myenv: mlx-lm-310
# pip install transformers accelerate
# https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct
# 2024.4.28 download

# os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"


# 指定LLM的位置，示例中给出了本地保存的模型。
# 如果只提供模型名称 “meta/Meta-Llama-3-8B-Instruct”
# 则 pipeline 会自动从 huggingface 上下载并缓存模型。
# 由于模型文件比较大，下载较慢，建议提前下载好模型。
# model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
model_id = "/Users/jingwu/janewu/llm-model/llama/meta/Meta-Llama-3-8B-Instruct"

start_time = datetime.now()

# 加载模型
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="cpu",   # auto （device_map 确保模型被移动到您的GPU(s)上，如果有的话。）
)

# 使用 AutoTokenizer 加载一个分词器
# 预处理文本输入
tokenizer = AutoTokenizer.from_pretrained(model_id)

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who are you?"},
]

input_ids = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_tensors="pt"
).to(model.device)


terminators = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

# 调用generate()方法来返回生成的token
outputs = model.generate(
    input_ids,
    max_new_tokens=256,  # 返回的最大新tokens数量
    eos_token_id=terminators,
    do_sample=True,
    temperature=0.6,
    top_p=0.9,
    pad_token_id=tokenizer.eos_token_id  # Setting `pad_token_id` to `eos_token_id`:128001 for open-end generation.
)

# 输出 转换为文本
response = outputs[0][input_ids.shape[-1]:]
print(tokenizer.decode(response, skip_special_tokens=True))

seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
print(f"total spend: {seconds.count()} seconds")


# q1 = "Who are you?"
# Nice to meet you! I am LLaMA, a helpful assistant developed by Meta AI that can understand and respond to human input in a conversational manner. I'm here to assist you with any questions, tasks, or topics you'd like to discuss. I can provide information on a wide range of subjects, from science and history to entertainment and culture. I can also help with language-related tasks such as language translation, text summarization, and even creative writing. My goal is to be a helpful and informative companion, so feel free to ask me anything!
# total spend: 254 seconds
