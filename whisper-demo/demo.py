import torch
import whisper

from datetime import datetime
from dateutil import rrule


def do_transcribe(filename, fp16):
    start_time = datetime.now()
    result = model.transcribe(filename, fp16=fp16)
    print(result["text"])
    seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
    print(f"total spend: {seconds.count()} seconds")


def do_translate(filename, fp16):
    start_time = datetime.now()
    result = model.transcribe(filename, fp16=fp16, language='english', verbose=False)
    print(result["text"])
    seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
    print(f"total spend: {seconds.count()} seconds")


# tiny base small medium large
# device = torch.device('cpu')
model = whisper.load_model("small")  # , device=device)

if __name__ == '__main__':
    fileList = [
        '../resources/w1-en.mp3',
        '../resources/w1-cn.mp3',
        '../resources/story.mp3'
    ]
    for fn in fileList:
        do_transcribe(fn, fp16=False)

    print('==========')
    # 翻译
    for fn in fileList[1:]:
        do_translate(fn, fp16=False)

    print('【END】.')
