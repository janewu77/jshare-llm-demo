import gradio as gr
import openai


def demo_gpt35_turbo_chatcompletion(inputs, openai_api_key, chatbot=[], history=[]):
    openai.api_key = openai_api_key
    system_prompt = '''以大话西游里的唐僧的风格回复问题。'''
    messages = [{"role": "system", "content": system_prompt}]
    # for data in chatbot:
    #     messages.append({"role": "user", "content": data[0]})
    #     messages.append({"role": "assistant", "content": data[1]})
    messages.append({"role": "user", "content": inputs})
    res = openai.ChatCompletion.create(
        temperature=1,
        model="gpt-3.5-turbo",  # 指定模型
        messages=messages
    )
    reply = res['choices'][0]['message']['content']
    # reply = reply.encode('utf-8').decode('unicode_escape')
    # print(f'reply:{reply}')
    history = history + [[inputs, reply]]
    # print(f'history:{history}')
    yield chatbot + history, history


def reset_textbox():
    return gr.update(value='')


title = """<h1 align="center">🔥一位有特别魅力的人，和TA聊聊，看看能不能猜出TA是谁🔥</h1>"""
with gr.Blocks(css="""#col_container {width: 1000px; margin-left: auto; margin-right: auto;}
                #chatbot {height: 320px; overflow: auto;}""") as demo:
    gr.HTML(title)
    with gr.Column(elem_id="col_container"):
        openai_api_key = gr.Textbox(type='password', label="Enter your OpenAI API key here")
        chatbot = gr.Chatbot(elem_id='chatbot')  # c
        inputs = gr.Textbox(placeholder="Hi there!", label="Type an input and press Enter")  # t
        state = gr.State([])  # s
        b1 = gr.Button()

    gr.HTML("""<center>
            <a href="https://huggingface.co/spaces/janewu/hualao?duplicate=true">
            <img style="margin-top: 0em; margin-bottom: 0em" src="https://bit.ly/3gLdBN6" alt="Duplicate Space"></a>
            Powered by OPENAI
            </center>""")

    inputs.submit(demo_gpt35_turbo_chatcompletion, [inputs, openai_api_key, chatbot, state],
                  [chatbot, state], )
    b1.click(demo_gpt35_turbo_chatcompletion, [inputs, openai_api_key, chatbot, state],
             [chatbot, state], )
    b1.click(reset_textbox, [], [inputs])
    inputs.submit(reset_textbox, [], [inputs])

    demo.queue().launch(debug=True)
