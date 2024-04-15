

### install lib
```bsh
pip install git+https://github.com/huggingface/parler-tts.git
```

install torch for Mac
```bsh
pip3 install --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/nightly/cpu
```


### other
* env: tts_39
* english only
* 速度比较慢
* 无法让声音保持一致。（即description是一样的，但生成出来的声音仍然会不同）

### cpu VS. mps

parler_tts_mini_v0.1 on 64G M2 Max
| seconds of audio | cpu(seconds of generation)  | mps(seconds of generation) |
|------------------|------|-----|
| 1                | 7   | 10  |
| 3                |  13  |  17 |
| 7                |  30  |  44 |
| 9                |  41  |  194 |
| 18                | 71   | 308  |

