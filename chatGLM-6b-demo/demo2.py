import torch
from transformers import AutoTokenizer, AutoModel
from datetime import datetime
from dateutil import rrule

my_now = datetime.now()

DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
print(f"DEVICE:{DEVICE}")

chatglm_path = '/Users/jingwu/janewu/llm-model/20230603/chatglm-6b'
# chatglm_path = '/Users/jingwu/janewu/llm-model/chatglm-6b'
tokenizer = AutoTokenizer.from_pretrained(chatglm_path, trust_remote_code=True, revision="v1.1.0")
model = AutoModel.from_pretrained(chatglm_path, trust_remote_code=True, revision="v1.1.0").half().to(DEVICE)
# model = load_model_on_gpus("THUDM/chatglm-6b", num_gpus=2)

model = model.eval()

# 一个推理的例子
q = '''
买了一只股票，先涨了10%，再降10%，最终的盈亏情况如何？请给出具体计算过程和结论。
think step by step
'''
# 如果想要在10年内实现投资10倍的收益，每年的收益率需要达到多少？请给出具体计算过程和结论。
response, history = model.chat(tokenizer, q, history=[])
print(response)
print(f"[total spend]: {rrule.rrule(freq=rrule.SECONDLY, dtstart=my_now, until=datetime.now()).count()} seconds")
