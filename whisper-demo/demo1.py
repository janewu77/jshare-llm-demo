import torch
import whisper
from datetime import datetime
from dateutil import rrule

start_time = datetime.now()
device = torch.device('mps')
model = whisper.load_model("base")

# load audio and pad/trim it to fit 30 seconds
audio = whisper.load_audio("../resources/w1-cn.mp3")

audio = whisper.pad_or_trim(audio)

# make log-Mel spectrogram and move to the same device as the model
mel = whisper.log_mel_spectrogram(audio)

# detect the spoken language
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")

# decode the audio
# translate
options = whisper.DecodingOptions(task='transcribe', fp16=False)
result = whisper.decode(model, mel, options)

# print the recognized text
print(result.text)
seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
print(f"total spend: {seconds.count()} seconds")
