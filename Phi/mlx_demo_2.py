from mlx_lm import load, generate

# pip install mlx-lm
# myenv: mlx-lm-310
# https://huggingface.co/mlx-community/Phi-3-mini-128k-instruct-8bit
# 2024.04.26

# pip install mlx-lm
# mlx-lm >=0.12.0
from mlx_lm import load, generate

# "mlx-community/Phi-3-mini-128k-instruct-8bit"
# model_path = "/Users/jingwu/janewu/llm-model/Phi-3/mlx/Phi-3-mini-128k-instruct-8bit"

model_path = "/Users/jingwu/janewu/llm-model/Phi-3/mlx/jw/Phi-3-mini-128k-instruct"
# model_path = "/Users/jingwu/janewu/llm-model/Phi-3/mlx/jw/Phi-3-mini-128k-instruct-8bit"


def do_generate():
    model, tokenizer = load(model_path)
    prompt1 = "hello"
    prompt2 = "Write a story about Einstein"
    prompt_sys = "始终用中文回复"
    chat_prompt = f'''<|system|>\n{prompt_sys}<|end|>\n<|user|>\n{prompt2}<|end|>\n<|assistant|>'''
    # chat_prompt = f"<|user|>\n{prompt1}<|end|>\n<|assistant|>"
    response = generate(model, tokenizer, prompt=chat_prompt, verbose=False)
    print(response, end="\n\n\n")


if __name__ == "__main__":

    do_generate()
    pass

# mlx/Phi-3-mini-128k-instruct-8bit
# Prompt: 43.352 tokens-per-sec
# Generation: 71.164 tokens-per-sec

# jw/Phi-3-mini-128k-instruct
# Prompt: 35.751 tokens-per-sec
# Generation: 41.192 tokens-per-sec

# jw/Phi-3-mini-128k-instruct-8bit
# Prompt: 59.340 tokens-per-sec
# Generation: 74.900 tokens-per-sec
