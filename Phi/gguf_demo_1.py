from llama_cpp import Llama

# Simple inference example
# pip install llama-cpp-python

# "./Phi-3-mini-4k-instruct-q4.gguf"
# model_path = "/Users/jingwu/janewu/llm-model/Phi-3/Phi-3-mini-4k-instruct-gguf/Phi-3-mini-4k-instruct-fp16.gguf"
model_path = "/Users/jingwu/janewu/llm-model/Phi-3/Phi-3-mini-4k-instruct-gguf/Phi-3-mini-4k-instruct-q4.gguf"


llm = Llama(
  model_path=model_path,  # path to GGUF file
  n_ctx=4096,  # The max sequence length to use - note that longer sequence lengths require much more resources
  n_threads=8,  # The number of CPU threads to use, tailor to your system and the resulting performance
  n_gpu_layers=35,  # The number of layers to offload to GPU, if you have GPU acceleration available. Set to 0 if no GPU acceleration is available on your system.
  verbose=False
)

prompt = "How to explain Internet to a medieval knight?"
output = llm(
  f"<|user|>\n{prompt}<|end|>\n<|assistant|>",
  max_tokens=1024,  # Generate up to 1024 tokens
  stop=["<|end|>"],
  echo=True,  # Whether to echo the prompt
)

print(output['choices'][0]['text'])


