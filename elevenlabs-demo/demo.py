from datetime import datetime

from dateutil import rrule

from elevenlabs import play
from elevenlabs import voices, generate
my_now = datetime.now()

# audio = generate(
#   text="Hi! My name is Bella, nice to meet you!",
#   voice="Bella",
#   model="eleven_monolingual_v1"
# )

audio = generate(
    text="¡Hola! Mi nombre es Arnold, encantado de conocerte!",
    voice="Arnold",
    model='eleven_multilingual_v1'
)
# voices = voices()
# print(voices)
# model="eleven_monolingual_v1"
# text="Hi! My name is Bella, nice to meet you!",Clyde
# audio = generate(
#   text="我是东圆有线网络有限公司的在线AI客服，由公司的开发团队开发。很抱歉，我无法提供开发者的联系方式。",
#   voice="Clyde",
#   model='eleven_multilingual_v2',
# )
#
play(audio)

print(f"[total spend]: {rrule.rrule(freq=rrule.SECONDLY, dtstart=my_now, until=datetime.now()).count()} seconds")
