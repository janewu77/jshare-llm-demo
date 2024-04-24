from transformers import AutoTokenizer, AutoModelForCausalLM
import os

from datetime import datetime
from dateutil import rrule

# pip install accelerate
# myenv: mlx-lm-310
# https://huggingface.co/shenzhi-wang/Llama3-8B-Chinese-Chat
# 2024.4.23 download
# too slow on Mac

# os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
model_id = "/Users/jingwu/janewu/llm-model/llama/Llama3-8B-Chinese-Chat"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id, torch_dtype="auto", device_map="cpu" # auto cpu
)


def llama3ChineseChat(prompt):
    start_time = datetime.now()

    messages = [
        # {"role": "system", "content": "You are Llama3-8B-Chinese-Chat, which is finetuned on Llama3-8B-Instruct with Chinese-English mixed data by the ORPO alignment algorithm. You, Llama3-8B-Chinese-Chat, is developed by Shenzhi Wang (王慎执 in Chinese). You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]

    input_ids = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt")\
        .to(model.device)

    outputs = model.generate(
        input_ids,
        max_new_tokens=1024,
        do_sample=True,
        temperature=0.8,
        top_p=0.9,
    )
    response = outputs[0][input_ids.shape[-1]:]
    print(tokenizer.decode(response, skip_special_tokens=True))

    seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
    print(f"total spend: {seconds.count()} seconds")


if __name__ == "__main__":
    prompt5 = '''
    我们将阅读一个场景，然后对其进行讨论。

    场景：
    小红和小明有一个共享的 Dropbox 文件夹。
    小红在 /shared_folder/photos 里放了一个叫做 'photo.png' 的文件。
    小明注意到小红把文件放在那里，并将文件移动到 /shared_folder/tmp。
    他没有告诉小红这件事，Dropbox 也没有通知小红。

    提问: 
    现在小红想打开 'photo.png'。她会去哪个文件夹里寻找它？
    '''
    prompt4 = '''
    买了一只股票，先涨了10%，再降10%，最终的盈亏情况如何？请给出具体计算过程和结论。
    think step by step
    '''

    llama3ChineseChat(prompt4)

# Prompt:
#     买了一只股票，先涨了10%，再降10%，最终的盈亏情况如何？请给出具体计算过程和结论。
#     think step by step
#
# Response:
# 让我们来一步一步地计算股票的最终盈亏情况。
#
# 假设你购买了一股股票，每股价值100美元。
#
# 1. 股票价格上涨10%：
#
# 新价格 = 100美元 x (1 + 0.10)
# 新价格 = 110美元
#
# 所以，你的股票现在价值110美元。
#
# 2. 股票价格下跌10%：
#
# 新价格 = 110美元 x (1 - 0.10)
# 新价格 = 99美元
#
# 所以，你的股票现在价值99美元。
#
# 3. 计算盈亏情况：
#
# 盈亏 = (股票当前价值 - 股票购买价格) x 股票数量
# 盈亏 = (99美元 - 100美元) x 1股
# 盈亏 = -1美元
#
# 你卖出股票时损失了1美元。
#
# 因此，购买了一只股票，先涨了10%，然后跌了10%的最终盈亏情况是亏损1美元。
# total spend: 493 seconds