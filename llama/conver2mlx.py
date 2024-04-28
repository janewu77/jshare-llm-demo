from mlx_lm import convert

# 生成mlx的格式
# model_source = "shenzhi-wang/Llama3-8B-Chinese-Chat"
# model_source = "/Users/jingwu/janewu/llm-model/llama/Llama3-8B-Chinese-Chat"
model_source = "/Users/jingwu/janewu/llm-model/llama/meta/Meta-Llama-3-8B-Instruct"
mlx_path = "mlx/Meta-Llama-3-8B-Instruct"
convert(model_source, mlx_path, quantize=True)

