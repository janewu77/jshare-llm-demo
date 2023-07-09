import cfg.cfg

import openai
import requests
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored
from datetime import date

import my_funcs

GPT_MODEL = "gpt-3.5-turbo-0613"
# gpt-3.5-turbo-16k-0613


@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, functions=None, function_call=None, model=GPT_MODEL):

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }
    json_data = {"model": model, "messages": messages, "temperature": 0, "user": "dad3"}
    if functions is not None:
        json_data.update({"functions": functions})
    if function_call is not None:
        json_data.update({"function_call": function_call})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


def pretty_print_conversation(messages):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }
    formatted_messages = []
    for message in messages:
        if message["role"] == "system":
            formatted_messages.append(f"system: {message['content']}\n")
        elif message["role"] == "user":
            formatted_messages.append(f"user: {message['content']}\n")
        elif message["role"] == "assistant" and message.get("function_call"):
            formatted_messages.append(f"assistant: {message['function_call']}\n")
        elif message["role"] == "assistant" and not message.get("function_call"):
            formatted_messages.append(f"assistant: {message['content']}\n")
        elif message["role"] == "function":
            formatted_messages.append(f"function ({message['name']}): {message['content']}\n")
    for formatted_message in formatted_messages:
        print(
            colored(
                formatted_message,
                role_to_color[messages[formatted_messages.index(formatted_message)]["role"]],
            )
        )




# Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous.
messages = []
# messages.append({"role": "system", "content": f'''
# 今天: {date.today()}\n
# 不要对插入到函数中的值做出假设。如果用户请求不明确，应该寻求澄清。
# 如果用户的问题，没有任何函数可以响应，则回复无法处理。
# 对于缺失的values请使用默认值。请按照参数格式给出结果。
# '''})
# Don't make assumptions about what values to plug into functions.
# Ask for clarification if a user request is ambiguous.
# messages.append({"role": "system", "content": f'''
# Today: {date.today()}
# For missing values, please use default values. Please provide the results according to the format of the parameters.
# Let's think step by step.
#
# For missing values, please use default values. Please provide the results according to the format of the parameters.
# 根据user信息判断属于哪个函数可以处理，当函数的参数是数组时，表示需要整理多出条信息。
# '''})
messages.append({"role": "system", "content": f'''
Today: {date.today()}
user_id: userX343
Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous.
'''})


def print_result(respJson):
    finish_reason = ''
    if 'finish_reason' in respJson["choices"][0]:
        finish_reason = respJson["choices"][0]["finish_reason"]
    print(f"finish_reason:{finish_reason}")

    assistant_message = respJson["choices"][0]["message"]
    if finish_reason == 'function_call':
        func_name = assistant_message["function_call"]['name']
        print(f"func_name:{func_name}")

    print(f"assistant response :{assistant_message}")


def do_chat(msg):
    messages.append({"role": "user", "content": msg})
    chat_response = chat_completion_request(
        messages, functions=my_funcs.functions,
        # function_call={"name": "accountant"}
    )

    json_data = chat_response.json()
    # json_data = chat_response
    print("======")
    if "error" in json_data:
        print("The JSON contains an error:", json_data["error"])
        return

    print(f"user:{msg}")
    print(f"  respJson:{json_data}")
    # print("\n\n\n")
    assistant_message = json_data["choices"][0]["message"]
    messages.append(assistant_message)

    print_result(json_data)


if __name__ == '__main__':
    # 下周一去超市买点水果
    do_chat("下周一去超市买点水果")
    # 今天买了二斤桔子 30元1斤 咖啡30元 昨天收到工资3000元
    do_chat("买了二斤桔子 30元1斤 买咖啡花了20.3元 用支付宝付的 上周收到工资3000元")
    # do_chat("后天去参加小张的婚礼")
    # do_chat("你最近怎么样？")

    print("\n\n\n")
    # pretty_print_conversation(messages)

