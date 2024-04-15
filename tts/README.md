
# 说明
把几个tts汇总到这个目录下
coqui, parler,
edge, openai, 


# 环境安装
env: tts_39

```bsh
日期时间
pip install python-dateutil

播放声音
pip install pygame

声音格式用
pip install pydub
//sudo apt-get install ffmpeg

```



## edge tts

### install
```commandline
pip install edge-tts
```


## coqui tts

```commandline
pip install TTS
```

### coqui tts 模型文件&声音样本目录
model_path = "/Users/jingwu/janewu/llm-model/coqui/XTTS-v2"


## openai tts
Name: openai
Version: 1.14.2
```commandline
pip install openai
```


## parler tts
Name: parler_tts
Version: 0.1
```bsh
pip install git+https://github.com/huggingface/parler-tts.git
```