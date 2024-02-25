from transformers import AutoModelForCausalLM, AutoTokenizer
from datetime import datetime
from dateutil import rrule

device = "mps"  # the device to load the model onto
# model_id = "/Users/jingwu/janewu/llm-model/mistralai/Mistral-7B-Instruct-v0.1"
model_id = "/Users/jingwu/janewu/llm-model/mistralai/Mistral-7B-Instruct-v0.2"
print(f"model_id:{model_id}")
model = AutoModelForCausalLM.from_pretrained(model_id)
tokenizer = AutoTokenizer.from_pretrained(model_id)

# messages = [
#     {"role": "user", "content": "What is your favourite condiment?"},
#     {"role": "assistant", "content": "Well, I'm quite partial to a good squeeze of fresh lemon juice. It adds just the right amount of zesty flavour to whatever I'm cooking up in the kitchen!"},
#     {"role": "user", "content": "Do you have mayonnaise recipes?"}
# ]
#
# q = '''
# 我们将阅读一个场景，然后对其进行讨论。
#
# 场景：
# 小红和小明有一个共享的 Dropbox 文件夹。
# 小红在 /shared_folder/photos 里放了一个叫做 'photo.png' 的文件。
# 小明注意到小红把文件放在那里，并将文件移动到 /shared_folder/tmp。
# 他没有告诉小红这件事，Dropbox 也没有通知小红。
#
# 提问:
# 现在小红想打开 'photo.png'。她会去哪个文件夹里寻找它？
# '''
# q2 = '''
# 买了一只股票，先涨了10%，再降10%，最终的盈亏情况如何？请给出具体计算过程和结论。
# let's think step by step
# '''
# q3 = '''
# 小明的爸爸有三个儿子，大儿子叫大宝，二儿子叫二宝，三儿子叫什么？
# '''
q4 = '''请以春天为主题，写一首五言绝句'''
#
# q5 = '''
# We will read about a scenario, and then have a question and answer session about it.
# Scenario:
#
# Tom just lost his ZURFIN, but he didn’t tell Adam.
#
# Adam starts talking to him about how much he loves his ZURFIN, and notices that Tom
# makes a sad face.
#
# Q: What does Adam think causes Tom’s sad face?
# '''
# q6 = '''
# Conversation:
#
# Mark: I don't like how you treated Jack last night
# Judy: Did you see what he was doing? He hit his brother on the head!
#
# Mark: That doesn't justify you yelling at him
#
# Judy: What do you want me to do? Let him beat his brother up and say nothing?
#
# Mark: No, I don't
# Judy: Then why are you defending him?
#
# Q: What does Mark's intent seem to be?
# '''
#
# q7='''
# word: Mistral
# * explain the word in detail in English
# * explain examples in English
# * 用中文解释单词的详细意思
# '''
# # messages = [
# #     {"role": "user", "content": "你好"},
# #     {"role": "assistant", "content": "你好！我很高兴能在这里遇到您！如果您有任何问题或需要帮助，请随时告诉我。"},
# #     {"role": "user", "content": q5},
# #
# # ]
messages = [
    {"role": "user", "content": q4}
]


encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")

model_inputs = encodeds.to(device)
model.to(device)

start_time = datetime.now()
# generated_ids = model.generate(model_inputs, max_new_tokens=1000, do_sample=True)
generated_ids = model.generate(model_inputs, max_new_tokens=1000, do_sample=True, pad_token_id=tokenizer.eos_token_id)
decoded = tokenizer.batch_decode(generated_ids)
print(decoded[0])


seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
print(f"total spend: {seconds.count()} seconds")

'''
0.1

q5
Q: What does Adam think causes Tom’s sad face?
 [/INST] Adam likely assumes that Tom's sad face is caused by something related to the ZURFIN, such as Tom losing it or having a negative experience with it. Adam may not know that Tom actually lost his ZURFIN, but is trying to understand what could be causing Tom's sad expression.</s>
total spend: 13 seconds
 [/INST] Adam likely thinks that Tom is upset because he lost his ZURFIN, as Adam's conversation about loving his ZURFIN and noticing that Tom was making a sad face leads to this conclusion.</s>
total spend: 8 seconds

q6
Q: What does Mark's intent seem to be?
 [/INST] Mark's intent is to hold both Jack and Judy accountable for their actions, and to make sure that justice is served. Mark is not defending Jack just because he didn't like how Judy treated him, but because he believes that hitting someone on the head is wrong and unacceptable. Mark is also concerned about the consequences of Judy's behavior, which could lead to a more serious situation if not handled properly.</s>
total spend: 19 seconds
 [/INST] Mark's intent seems to be to express his disagreement with Judy's behavior and to defend Jack's actions to some extent. He may be trying to find a middle ground or a more balanced perspective on the situation.</s>
total spend: 9 seconds


'''

'''
0.2
q5
Q: What does Adam think causes Tom’s sad face?
 [/INST] A: Based on the information given in the scenario, Adam might think that Tom is sad because he's missing his ZURFIN or feeling sad about losing it, not realizing that Tom has already lost it and hasn't shared that information with him yet.</s>
 [/INST] A: Based on the information provided in the scenario, Adam might think that Tom is also sad about losing his ZURFIN, as he expresses his own love for it and notices Tom's reaction. However, it's important to note that this is just an assumption, as Tom hasn't explicitly shared that he lost his ZURFIN with Adam.</s>
total spend: 13 seconds

q6
Q: What does Mark's intent seem to be?
 [/INST] Mark's intent seems to be expressing his disagreement with Judy's reaction to Jack's misbehavior and advocating for a more measured response instead of yelling at Jack. He is not defending Jack's actions, but rather the way Judy handled the situation.</s>
 [/INST] Mark's intent seems to be that he doesn't approve of Judy yelling at Jack, but he also doesn't condone Jack's violent behavior towards his brother. He wants both issues to be addressed without escalating the situation further.</s>

Mistral-7B-Instruct-v0.2

[INST] 请以春天为主题，写一首五言绝句 [/INST] 
春日风拂面，小兰散烟开，心似水之流，时速慵悠地，日短夜长到花霏。 

[INST] 请以春天为主题，写一首五言绝句 [/INST] 
春雨洒地绿，新苗伸向天，柔和欢笑开，鹦鹉吐玉绿，悠闲地待时流。


<s> [INST] 请以春天为主题，写一首五言绝句 [/INST] 春风起，玉树香，笑容照耩，绿芳草，人生光年长。

Translation:
With spring wind, jade tree fragrance, sun shining on smiling faces,
Green grass adorned, life's years extend in grace.</s>


'''