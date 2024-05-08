import cfg.cfg
import openai


def demo_gpt(stream=False):
    system_prompt = '''
    You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible. 
    请记录支出与收入信息。
    当有支出信息时，请记录支出明细（事项、单价、数量、金额)和总支出。
    当有收入信息时，请记录收入明细（事项、金额)和总收入。
    '''

    # 这是一段随手编的文字。模拟记录了多笔琐碎的收入与支出。
    # 有二点可以注意一下：1.文字里故意包含了一些语病。2.里面还有需要计算的金额。
    # 模型将按照“system”的规则与要求，将这段文字进行重新组织后输出。
    input_content = '''
    今天是2023-3-4.
    刚才买了一杯3元的咖啡，买酸奶花了5元，还买了2斤, 15元1斤的小桔子，和朋友一起吃饭又花了300.13元。
    酸奶是直接付的现金，其他是用花呗支付的。
    早上小陈还把上周的我垫付的外卖的钱给了我，一共8元。上午卖苹果收款2028元。昨天收到工资821元。
    '''

    req = {
        "temperature": 0,
        "model": "gpt-3.5-turbo",  # 指定模型
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_content}
        ],
        "stream": stream
    }
    if stream:
        # openai 1.26.0
        req["stream_options"] = {"include_usage": True}

    res = openai.chat.completions.create(**req)
    if stream:
        for chunk in res:
            # print(chunk)
            if len(chunk.choices) > 0:
                print(chunk.choices[0].delta.content, end='')
            else:
                usage = chunk.usage
                print(f"\n{usage}")
    else:
        print(res.usage)
        # CompletionUsage(completion_tokens=133, prompt_tokens=274, total_tokens=407)

        reply = res.choices[0].message.content
        # reply = res['choices'][0]['message']['content']
        # reply = reply.encode('utf-8').decode('unicode_escape')
        print(reply)


if __name__ == '__main__':
    demo_gpt(stream=True)

