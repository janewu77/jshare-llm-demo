
# llama 3 Demo

## env mlx-lm-310
```Shell
conda create --name mlx-lm-310 python=3.10
```

### install apple PyTorch-Nightly
```Shell
pip3 install --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/nightly/cpu

```

### install mlx-lm
```Shell
pip install mlx-lm
```
Name: mlx-lm
Version: 0.10.0
Summary: LLMs on Apple silicon with MLX and the Hugging Face Hub


### install others
```Shell
pip install transformers accelerate

pip install python-dateutil

pip install llama-cpp-python
```


## run via cmd(mlx)
```Shell
python -m mlx_lm.generate --model /Users/jingwu/janewu/llm-model/llama/mlx/Meta-Llama-3-70B-Instruct-4bit --prompt "'can you make big profits by relying on an expert who does have the proper qualifications? how do you find a true expert? That task is no easier than picking the right investments.' 请把以上内容翻译成中文。" --temp 0.0 --max-tokens 256
#python -m mlx_lm.generate --model /Users/jingwu/janewu/llm-model/llama/Meta-Llama-3-70B-4bit --prompt "请把内容翻译成中文: 'can you make big profits by relying on an expert who does have the proper qualifications? how do you find a true expert? That task is no easier than picking the right investments.' " 

python -m mlx_lm.generate --model /Users/jingwu/janewu/llm-model/llama/mlx/Meta-Llama-3-70B-Instruct-4bit --prompt "Write a story about Einstein" --temp 0.0 --max-tokens 256
```


## gguf

Model file from: https://huggingface.co/QuantFactory/Meta-Llama-3-8B-Instruct-GGUF/blob/main/Meta-Llama-3-8B-Instruct.Q5_K_M.gguf
（5.73GB）

Used prompt:(in llamaFarm)
<|begin_of_text|><|start_header_id|>system<|end_header_id|>
A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. <|eot_id|><|start_header_id|>user<|end_header_id|>
{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>






