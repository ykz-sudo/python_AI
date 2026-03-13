import asyncio  # 导入异步IO库，用于支持异步编程
import os  # 导入操作系统接口模块，用于环境变量设置
import time  # 导入时间模块，用于计时功能

import dotenv  # 导入dotenv库，用于从.env文件加载环境变量
from langchain_core.messages import HumanMessage, SystemMessage  # 导入消息类型，用于构建对话
from langchain_openai import ChatOpenAI  # 导入OpenAI聊天模型接口

dotenv.load_dotenv()  # 从.env文件加载环境变量

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY1")  # 设置OpenAI API密钥环境变量
os.environ['OPENAI_BASE_URL'] = os.getenv("OPENAI_BASE_URL")  # 设置OpenAI API基础URL环境变量

# 初始化大模型
chat_model = ChatOpenAI(model="gpt-5-mini", temperature=1)  # 创建ChatOpenAI实例，使用gpt-5-mini模型

# 同步调用（对比组）
def sync_test():  # 定义同步测试函数
    messages1 = [SystemMessage(content="你是一位乐于助人的智能小助手"),  # 创建系统消息
                 HumanMessage(content="请帮我介绍一下什么是机器学习"), ]  # 创建用户消息
    start_time = time.time()  # 记录开始时间
    response = chat_model.invoke(messages1)  # 同步调用模型
    duration = time.time() - start_time  # 计算调用耗时
    print(f"同步调用耗时：{duration:.2f}秒")  # 打印耗时信息
    return response, duration  # 返回响应和耗时


# 异步调用（实验组）
async def async_test():  # 定义异步测试函数
    messages1 = [SystemMessage(content="你是一位乐于助人的智能小助手"),  # 创建系统消息
                 HumanMessage(content="请帮我介绍一下什么是机器学习"), ]  # 创建用户消息
    start_time = time.time()  # 记录开始时间
    response = await chat_model.ainvoke(messages1)  # 异步调用模型
    duration = time.time() - start_time  # 计算调用耗时
    print(f"异步调用耗时：{duration:.2f}秒")  # 打印耗时信息
    return response, duration  # 返回响应和耗时


# 运行测试
if __name__ == "__main__":  # 当脚本直接运行时执行以下代码
    # 运行同步测试
    sync_response, sync_duration = sync_test()  # 执行同步测试并获取结果
    print(f"同步响应内容: {sync_response.content[:100]}...\n")  # 打印同步响应的前100个字符

    # 运行异步测试
    async_response, async_duration = asyncio.run(async_test())  # 执行异步测试并获取结果
    print(f"异步响应内容: {async_response.content[:100]}...\n")  # 打印异步响应的前100个字符

    # 并发测试 - 修复版本
    print("\n=== 并发测试 ===")  # 打印并发测试标题
    start_time = time.time()  # 记录并发测试开始时间


    async def run_concurrent_tests():  # 定义并发测试异步函数
        # 创建3个异步任务
        tasks = [async_test() for _ in range(3)]  # 创建3个异步测试任务
        # 并发执行所有任务
        return await asyncio.gather(*tasks)  # 并发执行所有任务并等待所有结果


    # 执行并发测试
    results = asyncio.run(run_concurrent_tests())  # 运行并发测试并获取结果

    total_time = time.time() - start_time  # 计算并发测试总耗时
    print(f"\n3个并发异步调用总耗时: {total_time:.2f}秒")  # 打印并发测试总耗时
    print(f"平均每个调用耗时: {total_time / 3:.2f}秒")  # 打印平均每个调用的耗时
