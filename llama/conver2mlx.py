from mlx_lm import convert

# 把Llama3-8B-Chinese-Chat 生成mlx的格式
# model_source = "shenzhi-wang/Llama3-8B-Chinese-Chat"
model_source = "/Users/jingwu/janewu/llm-model/llama/Llama3-8B-Chinese-Chat"
mlx_path = "mlx/Llama3-8B-Chinese-Chat"
convert(model_source, mlx_path, quantize=True)

