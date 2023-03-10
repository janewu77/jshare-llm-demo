import cfg.cfg
import openai
from datetime import datetime
from dateutil import rrule


def demo_whisper_1_run():
    start_time = datetime.now()

    # file = open("resources/w1-cn.mp3", "rb")
    file = open("../resources/w1-en.mp3", "rb")
    transcription = openai.Audio.transcribe("whisper-1", file)
    file.close()
    print(transcription.get("text"))

    seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
    print(f"total spend: {seconds.count()} seconds")
    print('【END】.')


if __name__ == '__main__':
    demo_whisper_1_run()
