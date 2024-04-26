from mlx_lm import load, generate

# myenv: mlx-lm-310
# https://huggingface.co/mlx-community/Meta-Llama-3-70B-Instruct-4bit
# 2024.04.22 it's buggy

# model_path = "/Users/jingwu/janewu/llm-model/llama/mlx/Meta-Llama-3-70B-Instruct-4bit"
model_path = "/Users/jingwu/janewu/llm-model/llama/mlx/Meta-Llama-3-8B-Instruct-4bit"
model, tokenizer = load(model_path)

# prompt = "你好，你是谁?"
# prompt = "买了一只股票，先涨了10%，再降10%，最终的盈亏情况如何？请给出具体计算过程和结论。think step by step"
prompt = "Write a story about Einstein"

response = generate(model, tokenizer, prompt=prompt, verbose=True) # , max_tokens=512) # temp=0.0

# 70B-Instruct-4bit
# Prompt: 0.851 tokens-per-sec
# Generation: 5.634 tokens-per-sec

# 8B-Instruct-4bit
# Prompt: 27.541 tokens-per-sec
# Generation: 61.209 tokens-per-sec