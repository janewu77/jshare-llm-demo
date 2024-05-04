import transformers
import torch
import os
from datetime import datetime
from dateutil import rrule

# 使用 pipeline()
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

# Transformers pipeline
pipeline = transformers.pipeline(
    "text-generation",  # 指定任务类型，文本生成就是text-generation
    model=model_id,
    model_kwargs={"torch_dtype": "auto"},  # torch.bfloat16
    device_map="cpu",  # auto mps cpu 通常这里设为auto. 如果可以使用mps，在这里进行指定。
)

q1 = "who are you?"
q = '''
买了一只股票，先涨了10%，再降10%，最终的盈亏情况如何？请给出具体计算过程和结论。
think step by step
'''

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": q},
]

# 文本被预处理为模型可以理解的格式
prompt = pipeline.tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
)

terminators = [
    pipeline.tokenizer.eos_token_id,
    pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

# 预处理的输入被传递给模型，进行推理（生成）
outputs = pipeline(
    prompt,
    max_new_tokens=256,
    eos_token_id=terminators,
    do_sample=True,
    temperature=0.6,
    top_p=0.9,
    pad_token_id=pipeline.tokenizer.eos_token_id  # Setting `pad_token_id` to `eos_token_id`:128001 for open-end generation.
)

# 模型处理后输出最终人类可以理解的结果
print(outputs[0]["generated_text"][len(prompt):])

seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
print(f"total spend: {seconds.count()} seconds")


# q1 = "Who are you?"
# I'm a helpful assistant! I'm an artificial intelligence designed to assist and provide information to users. I can answer questions, provide definitions, give suggestions, and even have a conversation with you. I'm here to help with any topic you'd like to discuss, from science and history to entertainment and more. What's on your mind?
# total spend: 170 seconds

# q = '''
# 买了一只股票，先涨了10%，再降10%，最终的盈亏情况如何？请给出具体计算过程和结论。
# think step by step
# '''
#
# Let's break down the situation step by step:
#
# 1. The stock initially increases by 10%. This means the stock price increases by 10% of its original value.
#
# Let's say the original stock price is $100. The increase of 10% would be:
#
# $100 x 0.10 = $10
#
# So, the new stock price would be:
#
# $100 + $10 = $110
#
# 2. Then, the stock price decreases by 10%. This means the stock price decreases by 10% of its new value, which is $110.
#
# The decrease of 10% would be:
#
# $110 x 0.10 = $11
#
# So, the new stock price would be:
#
# $110 - $11 = $99
#
# 3. Now, let's calculate the profit or loss. To do this, we need to compare the original stock price ($100) with the final stock price ($99).
#
# The difference is:
#
# $99 - $100 = -$1
#
# Since the final stock price is lower than the original stock price, we have a loss. The loss is:
#
# -$1
#
# So, the net result is a loss of $1, or -1%.
#
# That's it! The calculation process is:
#
# Initial increase: $
# total spend: 575 seconds