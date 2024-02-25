from mlx_lm import load, generate

# mlx 优化过的模型,从mlx-community下载的
model_id = "/Users/jingwu/janewu/llm-model/gemma/quantized-gemma-7b-it"

model, tokenizer = load(model_id)
# prompt = "Write me a poem about Machine Learning."
# prompt = "你会中文吗？"
prompt_1 = '''
Large language models (LLMs) have demonstrated impressive performance in understanding language and executing complex reasoning tasks. However, LLMs with long context windows have been notorious for their expensive training costs and high inference latency. Even the most advanced models such as GPT-4 and Claude2 often make mistakes when processing inputs of over 100k tokens, a phenomenon also known as lost in the middle.

你是一位精通简体中文的专业翻译，尤其擅长将专业学术论文翻译成浅显易懂的科普文章。请将用户提供的英文段落翻译成中文，风格与中文科普读物相似。

    规则：
    - 翻译时要准确传达原文的事实和背景。
    - 即使意译也要保留原始段落格式，以及保留术语，例如 FLAC，JPEG 等。保留公司缩写，例如 Microsoft, Amazon, OpenAI 等。
    - 人名不翻译
    - 同时要保留引用的论文，例如 [20] 这样的引用。
    - 对于 Figure 和 Table，翻译的同时保留原有格式，例如：“Figure 1: ”翻译为“图 1: ”，“Table 1: ”翻译为：“表 1: ”。
    - 全角括号换成半角括号，并在左括号前面加半角空格，右括号后面加半角空格。
    - 输入格式为 Markdown 格式，输出格式也必须保留原始 Markdown 格式
    - 在翻译专业术语时，第一次出现时要在括号里面写上英文原文，例如：“生成式 AI (Generative AI)”，之后就可以只写中文了。
    - 以下是常见的 AI 相关术语词汇对应表（English -> 中文）：
        * Transformer -> Transformer
        * Token -> Token
        * LLM/Large Language Model -> 大语言模型
        * Zero-shot -> 零样本
        * Few-shot -> 少样本
        * AI Agent -> AI 智能体
        * AGI -> 通用人工智能

    策略：

    分三步进行翻译工作，并打印每步的结果：
    1. 根据英文内容直译，保持原有格式，不要遗漏任何信息
    2. 根据第一步直译的结果，指出其中存在的具体问题，要准确描述，不宜笼统的表示，也不需要增加原文不存在的内容或格式，包括不仅限于：
        - 不符合中文表达习惯，明确指出不符合的地方
        - 语句不通顺，指出位置，不需要给出修改意见，意译时修复
        - 晦涩难懂，不易理解，可以尝试给出解释
    3. 根据第一步直译的结果和第二步指出的问题，重新进行意译，保证内容的原意的基础上，使其更易于理解，更符合中文的表达习惯，同时保持原有的格式不变

    返回格式如下，"{xxx}"表示占位符：

    ### 直译
    {直译结果}

    ***

    ### 问题
    {直译的具体问题列表}

    ***

    ### 意译
    {意译结果}
'''
prompt_1_a = '''
大语言模型 (LLM) 在理解语言和执行复杂推理任务方面展示了令人印象深刻的性能。
然而，具有长上下文窗口的 LLM 在训练成本和推理延迟方面存在一些缺点。
即使是最先的模型，例如 GPT-4 和 Claude2，在处理超过 100k 字节的输入时也经常发生错误，这就是所谓的“丢失在中间”现象。
Prompt: 300.098 tokens-per-sec
Generation: 23.437 tokens-per-sec

'''

prompt = '''
Large language models (LLMs) have demonstrated impressive performance in understanding language and executing complex reasoning tasks. However, LLMs with long context windows have been notorious for their expensive training costs and high inference latency. Even the most advanced models such as GPT-4 and Claude2 often make mistakes when processing inputs of over 100k tokens, a phenomenon also known as lost in the middle.
请翻译以上段落，let's think step by step
'''

response = generate(model, tokenizer, prompt=prompt, verbose=True)
