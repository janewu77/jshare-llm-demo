run on Mac

## 资源
HF:
https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1
https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2
https://github.com/mistralai/mistral-src


## 安装包
This should not be required after transformers-v4.33.4.
Name: transformers
Version: 4.36.0.dev0
pip install git+https://github.com/huggingface/transformers


Name: torch
Version: 2.4.0.dev20240331
```Shell
# for Mac see:https://developer.apple.com/metal/pytorch/
pip3 install --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/nightly/cpu
```

其他包
pip install python-dateutil
pip install bitsandbytes


## 虚拟环境
mistral310: python3.10




