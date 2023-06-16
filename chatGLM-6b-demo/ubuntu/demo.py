import torch
from transformers import AutoTokenizer, AutoModel
from datetime import datetime
from dateutil import rrule

my_now = datetime.now()

# 指定本地模型所在路径
chatglm_path = '/mnt/data_500g/llm-models/chatglm-6b'
# DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
# print(f"DEVICE:{DEVICE}")

tokenizer = AutoTokenizer.from_pretrained(chatglm_path, trust_remote_code=True, revision="v1.1.0")
# 如果只有cpu就用float跑。如果有gpu，那就用cuda。这完全取决于服务器的配置。
model = AutoModel.from_pretrained(chatglm_path, trust_remote_code=True, revision="v1.1.0").float()
# model = AutoModel.from_pretrained(chatglm_path, trust_remote_code=True, revision="v1.1.0").half().cuda()
# 按需修改，目前只支持 4/8 bit 量化
# model = AutoModel.from_pretrained(chatglm_path, trust_remote_code=True).quantize(8).half().cuda()

model = model.eval()
response, history = model.chat(tokenizer, "你好?", history=[])
print(response)
print(f"[total spend]: {rrule.rrule(freq=rrule.SECONDLY, dtstart=my_now, until=datetime.now()).count()} seconds")

my_now = datetime.now()
response, history = model.chat(tokenizer, "晚上睡不着应该怎么办", history=[])
print(response)
print(f"[total spend]: {rrule.rrule(freq=rrule.SECONDLY, dtstart=my_now, until=datetime.now()).count()} seconds")
#
# my_now = datetime.now()
# response, history = model.chat(tokenizer, "晚上能喝咖啡不？", history=[])
# print(response)
# print(f"[total spend]: {rrule.rrule(freq=rrule.SECONDLY, dtstart=my_now, until=datetime.now()).count()} seconds")
#
# my_now = datetime.now()
# response, history = model.chat(tokenizer, "小明的爸爸有三个儿子，大儿子叫大宝，二儿子叫二宝，三儿子叫什么？", history=[])
# print(response)
# print(f"[total spend]: {rrule.rrule(freq=rrule.SECONDLY, dtstart=my_now, until=datetime.now()).count()} seconds")
