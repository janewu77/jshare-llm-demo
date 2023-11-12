import cfg.cfg
from openai import OpenAI
import time

client = OpenAI()


# Upload a file with an "assistants" purpose
def upload_file():
    file = client.files.create(
        file=open("model_3_owners_manual_asia_cn.pdf", "rb"),
        purpose='assistants'
    )
    print(file)
    return file.id


def create_assistant():
    file_id = upload_file()
    my_assistant = client.beta.assistants.create(
        instructions="根据附件内容回复用户的问题",
        name="assistant_demo_pdf",
        tools=[{"type": "code_interpreter"}, {"type": "retrieval"}],
        model="gpt-3.5-turbo-1106", #gpt-4-1106-preview
        file_ids=[file_id],
        description="for demo",
        metadata={"creator": "by tester"}
    )
    print(my_assistant)
    print("=========")
    return my_assistant.id


def get_thread():
    # 创建thread
    thread = client.beta.threads.create(
        metadata={"user_id": "user_demo"}
    )
    print(f"thread.id:{thread.id}")
    print("=======")
    return thread.id


def run_assistant(assistant_id, tread_id, q):
    if tread_id is None:
        tread_id = get_thread()

    # Add a Message to a Thread
    message = client.beta.threads.messages.create(
        thread_id=tread_id,
        role="user",
        content=q,
        metadata={"user_id": "user_demo_msg"}
    )

    # create run
    run = client.beta.threads.runs.create(
      thread_id=tread_id,
      assistant_id=assistant_id,
      # instructions="Please address the user as Jane Doe. The user has a premium account."
    )
    run_id = run.id
    retrieve_result(tread_id, run_id)


def retrieve_result(tread_id, run_id):
    in_progress = True
    run = None
    while in_progress:
        run = client.beta.threads.runs.retrieve(
            thread_id=tread_id,
            run_id=run_id
        )
        print(f"run:{run}")
        print(f"run.id:{run.id}")
        print(f"run.status:{run.status}")
        print("=======")
        in_progress = run.status in ("in_progress", "queued")
        if in_progress:
            time.sleep(1)

    if run.status == "completed":
        show_latest_messages(tread_id)

    print(f"run.status:{run.status}")
    print(f"[end]")


def show_all_messages(tread_id, is_asc=True):
    messages = client.beta.threads.messages.list(thread_id=tread_id)
    message_list = reversed(messages.data) if is_asc else messages.data
    for msg in message_list:
        _show_message(msg)


def show_latest_messages(tread_id):
    messages = client.beta.threads.messages.list(thread_id=tread_id, order="asc")
    for msg in messages.data[0:1]:
        _show_message(msg)


def _show_message(msg):
    # messages = client.beta.threads.messages.list(thread_id=tread_id)
    # print(f"messages:{messages}")
    # print(f"messages.data[0].role:{messages.data[0].role}")
    # print(f"messages.data[0].content[0].text:{messages.data[0].content[0].text.value}")
    # print(f"messages.data[0].role:{messages.data[0].role}")
    # for msg in messages.data[0:1]:
    print(f"msg:{msg}")
    print(f"{msg.role}:")
    i = 0
    for msg_content in msg.content:
        print(f"{i}>>>")
        i = i + 1
        # msg_content_text = msg_content.text

        annotations = msg_content.text.annotations
        citations = []
        # Iterate over the annotations and add footnotes
        for index, annotation in enumerate(annotations):
            # Replace the text with a footnote
            msg_content.text.value = msg_content.text.value.replace(annotation.text, f' [{index}]')

            # Gather citations based on annotation attributes
            if (file_citation := getattr(annotation, 'file_citation', None)):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(f'[{index}] {file_citation.quote} from {cited_file.filename}')
            elif (file_path := getattr(annotation, 'file_path', None)):
                cited_file = client.files.retrieve(file_path.file_id)
                citations.append(f'[{index}] Click <here> to download {cited_file.filename}')
                # Note: File download functionality not implemented above for brevity

        if len(citations) > 0:
            msg_content.text.value += '\n' + '\n'.join(citations)

        print(f"{msg_content.text.value}")
        print("----------")


if __name__ == '__main__':
    # create_assistant()
    # assistant_id = "asst_aalFqbUCq7KcGaMr0Gb4s8J2"
    # tread_id = get_thread()
    # run_assistant(assistant_id=assistant_id, tread_id=tread_id, q="支持几种类型的钥匙")
    # run_assistant(assistant_id=assistant_id, tread_id=tread_id, q="如何添加新手机钥匙")
    # thread_jXNO4P99TqZCfJS7b9TSUO5j
    show_all_messages("thread_6oTJ8yfzzxnpE85ostHne9uZ")
