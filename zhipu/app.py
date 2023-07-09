import cfg.cfg as cfg

from datetime import datetime
from dateutil import rrule
import zhipuai

zhipuai.api_key = cfg.zhipuai_api_key

# chatglm_lite chatglm_std
MODEL = "chatglm_lite"


def invoke_example(p):
    response = zhipuai.model_api.invoke(
        model=MODEL,
        prompt=[{"role": "user", "content": p}],
        top_p=0.7,
        temperature=0.9,
    )
    print(response)
    reply = response['data']['choices'][0]['content']
    return reply


if __name__ == '__main__':
    my_now = datetime.now()
    prompt = "hi, 你能做些什么？"
    response = invoke_example(prompt)
    print(response)
    print(f"[total spend]: {rrule.rrule(freq=rrule.SECONDLY, dtstart=my_now, until=datetime.now()).count()} seconds")
