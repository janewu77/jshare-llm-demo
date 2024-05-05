from mlx_lm import load, generate

# mlx-lm demo
# myenv: mlx-lm-310


# download from huggingface
# https://huggingface.co/mlx-community/Meta-Llama-3-70B-Instruct-4bit
# 2024.04.22 download it's buggy
# 2024.05.05 update model & lib. now it's fine
# model_path = "/Users/jingwu/janewu/llm-model/llama/mlx/Meta-Llama-3-70B-Instruct-4bit"
model_path = "/Users/jingwu/janewu/llm-model/llama/mlx/Meta-Llama-3-8B-Instruct-4bit"

# convert in local:
# convert from "/Users/jingwu/janewu/llm-model/llama/meta/Meta-Llama-3-8B-Instruct"
# convert: quantize=False
# model_path = "/Users/jingwu/janewu/llm-model/llama/mlx/jw/Meta-Llama-3-8B-Instruct"
# convert:  quantize=True, q_bits=4
# model_path = "/Users/jingwu/janewu/llm-model/llama/mlx/jw/Meta-Llama-3-8B-Instruct-q-4bit"


# load
model, tokenizer = load(model_path)

# prompt & conversion
# prompt = "你好，你是谁?"
# prompt = "买了一只股票，先涨了10%，再降10%，最终的盈亏情况如何？请给出具体计算过程和结论。think step by step"
# prompt = "Write a story about Einstein"
prompt = "who are you?"
# prompt = "hello"

messages = [
    {"role": "system", "content": "A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. "},
    {"role": "user", "content": prompt},
]
chat_template = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=False
)
# same as tokenizer.apply_chat_template
# chat_template = f'''<|begin_of_text|><|start_header_id|>system<|end_header_id|>
# A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. <|eot_id|><|start_header_id|>user<|end_header_id|>
# {prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
# '''

# generate
response = generate(model, tokenizer, prompt=chat_template, verbose=True, max_tokens=512)  # temp=0.0

# output
# 70B-Instruct-4bit
# Prompt: 15.810 tokens-per-sec
# Generation: 5.703 tokens-per-sec

# 8B-Instruct-4bit
# Prompt: 316.486 tokens-per-sec
# Generation: 65.956 tokens-per-sec


# JW/Meta-Llama-3-8B-Instruct
# Prompt: 127.624 tokens-per-sec
# Generation: 19.819 tokens-per-sec

# JW/Meta-Llama-3-8B-Instruct-q-4bit
# Prompt: 325.235 tokens-per-sec
# Generation: 58.611 tokens-per-sec
