from datetime import datetime

from dateutil import rrule
# from dateutil import rrule

from elevenlabs import play, set_api_key
from elevenlabs import voices, generate
my_now = datetime.now()

from elevenlabs import generate, stream

set_api_key("7a71c3d876f6a705ad4282aa201206f2")

t = "Hi! Of course, we can talk about snacks. What would you like to discuss?"
# t = "This is a... streaming voice!!",
audio_stream = generate(
  text=t,
  stream=True
)

stream(audio_stream)

print(f"[total spend]: {rrule.rrule(freq=rrule.SECONDLY, dtstart=my_now, until=datetime.now()).count()} seconds")
