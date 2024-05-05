from mlx_lm import convert

# Name: mlx-lm Version: 0.12.1
# 生成mlx的格式
# model_source = "shenzhi-wang/Llama3-8B-Chinese-Chat"
# model_source = "/Users/jingwu/janewu/llm-model/llama/Llama3-8B-Chinese-Chat"
model_source = "/Users/jingwu/janewu/llm-model/llama/meta/Meta-Llama-3-8B-Instruct"
mlx_path = "mlx/jw/Meta-Llama-3-8B-Instruct-q-4bit"
convert(model_source, mlx_path, quantize=True, q_bits=4)

