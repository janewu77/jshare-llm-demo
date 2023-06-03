# 🚀💻 FastAPI 介绍 🌟🧩

## 写在前面
最近在尝试一些可在笔记本上运行的语言模型时，需要写一些api让我的其他应用能使用这些本地模型。   
然后我发现了FastAPI。官方网站是这么介绍它的：FastAPI 是一个用于构建 API 的现代、快速（高性能）的 web 框架，使用 Python 3.6+ 并基于标准的 Python 类型提示。    
随后，不到5分钟，我发现它确实很fast，连学起来都很快。   
嗯，大概也只要5分钟。Let‘s just do it.

## 前提
    安装python 3.6+ 的环境

## 安装 FastAPI

    ```Shell
    pip install "fastapi[all]"
    ```

## 示例代码
    ```helloworld.py
    # 导入 fastapi & uvicorn
    import uvicorn
    from fastapi import FastAPI

    # 代码从这里开始，创建一个FastAPI实例
    app = FastAPI()
    
    # 第一个路由：著名的hello world
    @app.get("/")
    async def sayHello():
    return {"message": "Hello World"}

    # 让我们运行它吧
    if __name__ == '__main__':
        # 你也可以换一个port. 然后打开浏览器 访问：http://127.0.0.1:8000
        uvicorn.run(app, host='127.0.0.1', port=8000, workers=1)
    ```

运行这个文件后，打开浏览器 访问：http://127.0.0.1:8000，就能看见“Hello World”。    
它还自带了api文档：http://127.0.0.1:8000/docs     
如果你用过一些其他的框架，比如Django、Chalice等，我相信即使不加注释，你也能一眼看明白代码。是不是简单到惊人？  
好吧，反正我在5分钟之内就被它圈粉了。嗯， 更详细的使用说明，可以参阅官方文档。连接在文末。    
Enjoy it~~~


## 参考：
* [官网](https://fastapi.tiangolo.com/)   
* [github](https://github.com/tiangolo/fastapi)   
* [示例代码](https://github.com/janewu77/jshare-llm-demo/tree/main/fastapi-demo)

