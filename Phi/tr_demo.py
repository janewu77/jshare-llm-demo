import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from datetime import datetime
from dateutil import rrule
# pip install transformers accelerate


torch.random.manual_seed(0)

DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
print(f"DEVICE:{DEVICE}")

# "microsoft/Phi-3-mini-128k-instruct"
model_path = "/Users/jingwu/janewu/llm-model/Phi-3/Phi-3-mini-128k-instruct"
start_time = datetime.now()
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    device_map="cpu",  # "cuda mps cpu auto
    torch_dtype="auto",
    trust_remote_code=True,
)
tokenizer = AutoTokenizer.from_pretrained(model_path)

"What about solving an 2x + 3 = 7 equation?"
q = '''
买了一只股票，先涨了10%，再降10%，最终的盈亏情况如何？请给出具体计算过程和结论。
think step by step
'''
messages = [
    {"role": "system", "content": "You are a helpful digital assistant. Please provide safe, ethical and accurate information to the user."},
    {"role": "user", "content": "Can you provide ways to eat combinations of bananas and dragonfruits?"},
    {"role": "assistant", "content": "Sure! Here are some ways to eat bananas and dragonfruits together: 1. Banana and dragonfruit smoothie: Blend bananas and dragonfruits together with some milk and honey. 2. Banana and dragonfruit salad: Mix sliced bananas and dragonfruits together with some lemon juice and honey."},
    {"role": "user", "content": q},
]

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
)

generation_args = {
    "max_new_tokens": 500,
    "return_full_text": False,
    "temperature": 0.8,
    "do_sample": True,
}

output = pipe(messages, **generation_args)
print(output[0]['generated_text'])

seconds = rrule.rrule(freq=rrule.SECONDLY, dtstart=start_time, until=datetime.now())
print(f"total spend: {seconds.count()} seconds")

# To solve the equation 2x + 3 = 7, first, you need to isolate the variable x. You can begin by subtracting 3 from both sides of the equation which gives you 2x = 4. Then, you divide both sides by 2 to get the value of x. So, x = 2.
# total spend: 213 seconds