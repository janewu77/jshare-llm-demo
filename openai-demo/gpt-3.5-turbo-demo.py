import cfg.cfg
import openai


# gpt35_turbo的第一个简单demo
# 注意:使用 gpt-3.5-turbo 模型需要 OpenAI Python v0.27.0版本
def demo_gpt35_turbo_chatcompletion():
    # 新的接口增加了role的概念。
    # 在这个例子里，我把"system"当成一个指令员来使用了。它向模型说明了规则与要求。
    system_prompt = '''
    You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible. 
    请记录支出与收入信息。
    当有支出信息时，请记录支出明细（事项、单价、数量、金额)和总支出。
    当有收入信息时，请记录收入明细（事项、金额)和总收入。
    '''

    # 这是提供给模型的文字。模型将按照上面的规则与要求，将这段文字进行输出。
    input_content = '''
    今天是2023-3-4.
    刚才买了一杯3元的咖啡，买酸奶花了5元，还买了2斤, 15元1斤的小桔子，和朋友一起吃饭又花了300.13元。
    酸奶是直接付的现金，其他是用花呗支付的。
    早上小陈还把上周的我垫付的外卖的钱给了我，一共8元。上午卖苹果收款2028元。昨天收到工资821元。
    '''
    res = openai.ChatCompletion.create(
        temperature=0,
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_content}
        ]
    )
    print(res)

    reply = res['choices'][0]['message']['content']
    # reply = reply.encode('utf-8').decode('unicode_escape')
    print(reply)


if __name__ == '__main__':
    demo_gpt35_turbo_chatcompletion()
