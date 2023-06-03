# 导入 fastapi & uvicorn
import uvicorn
from fastapi import FastAPI

# 代码从这里开始，创建一个FastAPI实例
app = FastAPI()


# 第一个路由：著名的hello world
@app.get("/")
async def say_hello():
    return {"message": "Hello World"}


# 让我们运行它吧
if __name__ == '__main__':
    # 运行开发服务器 uvicorn
    # 指定ip和port. 然后打开浏览器 访问：http://127.0.0.1:8000
    uvicorn.run(app, host='127.0.0.1', port=8000, workers=1)
