# What
最近在学习LLM、OPENAI、langChain...等有趣的新技术。  
这个repo用来保存学习过程中的demo。

# openai-demo
* gpt-3.5-turbo-demo
* whisper-1-demo (中文/英文)

# bookkeeping
* 一个记帐的例子

#  hualao
* 放在hugging face上的一个简单demo

# 开始前的准备
- 申请OPENAI的KEY。 可以在网络上搜索如何申请key,相信你会找到答案的。    
- 准备好Python的开发环境(python 3.9)和工具(pycharm)   



## 环境 set up
安装 openai
```
$ pip install openai

$ pip freeze | grep openai >> requirements.txt
```

安装LangChain
```
$ pip install langchain[all]

$ pip freeze | grep langchain >> requirements.txt
```



## 正在使用的版本
```
langchain==0.0.98
openai==0.27.0
```

