# whisper run on local


## set environment

```commandline
conda create --name whisper310 python=3.10
```

```commandline
pip install -U openai-whisper
brew install ffmpeg
brew install rust
```

## run
```commandline
whisper ../resources/w1-cn.mp3 --model medium --device cpu
// 翻译
whisper ../resources/w1-cn.mp3 --language Chinese --task translate
```
