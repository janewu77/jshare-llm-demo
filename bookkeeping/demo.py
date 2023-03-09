import cfg.cfg
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain, SequentialChain
from bookkeeping import db


# 记帐的第一个DEMO(已废弃）
# base on 3.0

prompt_1 = '''
内容:{content}
用户:{username}
'''

prompt_1_expenditure = '''
假设你是一位严谨的记帐员,请根据内容区分收入与支出后，按要求进行记帐并输出json格式。如果你不知道，请回复不知道。
内容:{content}
用户:{username}
要求:记录支出明细（事项、单价、数量、金额)和总支出。
'''

prompt_1_income = '''
假设你是一位严谨的记帐员,请根据内容区分收入与支出后，按要求进行记帐并输出json格式。如果你不知道，请回复不知道。
用户:{username}
内容:{content}
要求:记录收入明细（事项、金额)和总收入。
'''

prompt_sql = '''
将内容生成SQL语句。
数据库表 daily_info 结构：
字段名｜类型
xid｜数字型 ｜ default: 5
item｜字符型 
price｜浮点数
count｜浮点数｜数量｜default:1
amount｜浮点数
user｜字符型｜用户
flag｜字符型｜标记｜'支出','收入'
pmethod | 字符型｜收付款方式
'''

prompt_sql_X = '''
数据库表 daily_info 结构：
字段名｜类型
id｜数字型 
item｜字符型 
price｜浮点数
count｜浮点数｜数量｜default:1
amount｜浮点数
user｜字符型｜用户
flag｜字符型｜标记｜'支出','收入'

将以下内容生成SQL语句。
{cjson}
'''
# Answer: Let's think step by step."""


# 生成一个llmChain
def _get_bookkeeping_chain_1(custom_prompt) -> LLMChain:
    llm = OpenAI(temperature=0)
    first_prompt = PromptTemplate(
        input_variables=["content", "username"],
        template=custom_prompt
    )
    chain_first = LLMChain(llm=llm, prompt=first_prompt, output_key="cjson", verbose=True)
    return chain_first


def _get_bookkeeping_chain_2(custom_prompt) -> LLMChain:
    llm = OpenAI(model='code-davinci-002', temperature=0)
    # model='code-davinci-002'
    first_prompt = PromptTemplate(
        input_variables=["cjson"],
        template=custom_prompt
    )
    chain_first = LLMChain(llm=llm, prompt=first_prompt, output_key="res_sql", verbose=True)
    return chain_first


# 根据用户输入，进行记帐，数据进行持久化
def bookkeeping_chain_run(ttype, custom_input, username='Jane Doe', is_persist=False):
    if ttype == 1:
        chain_first = _get_bookkeeping_chain_1(prompt_1_expenditure)
    else:
        chain_first = _get_bookkeeping_chain_1(prompt_1_income)

    # # 文字>sql
    chain_second = _get_bookkeeping_chain_2(prompt_sql)

    overall_chain = SequentialChain(
        chains=[chain_first, chain_second],
        input_variables=["content", "username"],
        # output_variables=["cjson", "ressql"],
        verbose=False)
    res_sql = overall_chain.run(content=custom_input, username=username)

    if is_persist:
        # 持久化
        db.run_sql(res_sql)
    else:
        print(res_sql)


if __name__ == '__main__':
    # demo2()
    # # 根据用户输入，进行记帐，将数据进行持久化
    custom_input_3 = "刚才买了一杯3元的咖啡，买酸奶花了5元，还买了2斤, 15元1斤的小桔子。"
    bookkeeping_chain_run(1, custom_input_3, "Mary Lee", False)
    #
    # custom_input_4 = "早上小陈还把上周的我垫付的外卖的钱给了我，一共8元。上午卖香蕉后收到钱2028元。昨天收到工资821元。"
    # bookkeeping_chain_run(2, custom_input_4, "老王", False)




