from datetime import datetime

from dateutil import rrule

from elevenlabs import play, set_api_key

from cfg.cfg import eleventlabs_api_key

my_now = datetime.now()

from elevenlabs import generate, stream

set_api_key(eleventlabs_api_key)

t = '我是东圆有线网络有限公司的在线AI客服，由公司的开发团队开发。很抱歉，我无法提供开发者的联系方式。'
# t = "Hi! Of course, we can talk about snacks. What would you like to discuss?"


# audio_stream = generate(
#   text=t,
#   voice="Bella",
#   model='eleven_monolingual_v1',
#   stream=True,
# )

# cn
audio_stream = generate(
  text=t,
  voice="Clyde",
  model='eleven_multilingual_v2',
  stream=True,
)

stream(audio_stream)

print(f"[total spend]: {rrule.rrule(freq=rrule.SECONDLY, dtstart=my_now, until=datetime.now()).count()} seconds")
