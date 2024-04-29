from mlx_lm import load, generate

# pip install mlx-lm
# myenv: mlx-lm-310
# https://huggingface.co/mlx-community/Phi-3-mini-128k-instruct-8bit
# 2024.04.26

# pip install mlx-lm
# mlx-lm >=0.12.0
from mlx_lm import load, generate

# "mlx-community/Phi-3-mini-128k-instruct-8bit"
model_path = "/Users/jingwu/janewu/llm-model/Phi-3/mlx/Phi-3-mini-128k-instruct-8bit"


def do_generate():
    model, tokenizer = load(model_path)

    prompt1 = "hello"
    # prompt2 = "Write a story about Einstein"
    prompt = f"<|user|>\n{prompt1}<|end|>\n<|assistant|>"
    response = generate(model, tokenizer, prompt=prompt, verbose=True)
    print(response, end="\n\n\n")

    # Prompt: 43.352 tokens-per-sec
    # Generation: 71.164 tokens-per-sec


def do_convert():
    from mlx_lm import convert
    model_path = "/Users/jingwu/janewu/llm-model/Phi-3/Phi-3-mini-128k-instruct"
    mlx_path = "mlx/jw/Phi-3-mini-128k-instruct-8bit"
    convert(model_path, mlx_path, q_bits=8, quantize=True)


if __name__ == "__main__":
    # do_convert()
    do_generate()
    pass

