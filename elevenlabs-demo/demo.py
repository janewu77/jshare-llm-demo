from datetime import datetime

from dateutil import rrule

from elevenlabs import play
from elevenlabs import voices, generate
my_now = datetime.now()

voices = voices()
print(voices)


# t = '我是东圆有线网络有限公司的在线AI客服，由公司的开发团队开发。很抱歉，我无法提供开发者的联系方式。'
t = "Hi! Of course, we can talk about snacks. What would you like to discuss?"

# audio = generate(
#   text="Hi! My name is Bella, nice to meet you!",
#   voice="Bella",
#   model="eleven_monolingual_v1"
# )

# cn
audio = generate(
  text=t,
  voice="Clyde",
  model='eleven_multilingual_v2',
)

play(audio)

print(f"[total spend]: {rrule.rrule(freq=rrule.SECONDLY, dtstart=my_now, until=datetime.now()).count()} seconds")
