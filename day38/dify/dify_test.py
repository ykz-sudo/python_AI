import requests
import json

# 响应返回模式
# 流式，基于SSE（Server-Sent Events）实现类似打字机输出方式的流式返回
STREAMING_MODE = "streaming"
# 阻塞式，等待执行完毕后返回结果（流程较长则可能会被中断）。由于Cloudflare限制，请求会在100秒超时无返回后中断
BLOCKING_MODE = "blocking"

# 工作流的API_KEY
API_KEY = "app-dHi7R1r4qp00IcUON7f7LQvk"
# Dify base_url，如果是本地部署，替换为 http://localhost/v1
BASE_URL = "https://api.dify.ai/v1"

# 工作流完成标志
WORKFLOW_FINISHED = "workflow_finished"
# 工作流成功标志
WORKFLOW_SUCCESS = "succeeded"


# 用于启动工作流
def stream_dify_workflow(target, api_key=API_KEY, base_url=BASE_URL, username="python_request", mode=STREAMING_MODE):
    # 拼接用于启动工作流的 url
    url = f"{base_url}/workflows/run"

    # 拼接头信息，包括API Key和数据类型
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # 拼接请求体
    payload = {
        "inputs": {"target": target},
        "response_mode": mode,
        "user": username
    }

    try:
        # 使用stream=True保持连接打开
        with requests.post(url, headers=headers, json=payload, stream=True) as response:
            if response.status_code != 200:
                print(f"请求失败，状态码: {response.status_code}")
                print(response.text)
                return

            print("=== 开始接收流式响应: ===")
            # 逐行读取服务器推送的数据
            for line in response.iter_lines():
                if line:
                    # 解码
                    decoded_line = line.decode('utf-8')

                    # 处理中文乱码，将Unicode转义格式处理为正常中文
                    fixed_line = decoded_line.encode("utf-8").decode("unicode_escape")

                    # 打印由二进制二进制解析为UTF-8后的响应
                    print(f"decoded_line: {decoded_line}")
                    # 解码后换行会导致日志非常乱，一般不打开
                    # print(f"fixed_line: {fixed_line}")
                    # print(fixed_line)

                    # 去除SSE格式前缀
                    if (decoded_line.startswith("data: ")):
                        decoded_line = decoded_line[6:]

                        try:
                            # 尝试解析为JSON
                            json_data = json.loads(decoded_line)
                            if (json_data.get("event") == WORKFLOW_FINISHED):
                                print("---> 工作流执行完毕 <---")
                                print(f"{json_data.get("data")=}")
                                data = json_data.get("data")
                                workflow_status = data.get("status")
                                if (workflow_status == WORKFLOW_SUCCESS):
                                    print("---> 工作流执行成功 <---")

                                    try:
                                        # 获取工作流最终输出
                                        result = data.get("outputs").get("output")

                                        # 返回结果
                                        return result
                                    except Exception as e:
                                        print("工作流输出解码错误: ", e)
                                        print("data: ", data)
                                        return None
                                else:
                                    print("---> 工作流执行失败 <---")
                                    return None
                        except Exception as e:
                            print("JSON解析错误: ", e)
                            return None

            print("=== 流式响应结束 ===")

    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")
        return None


if __name__ == "__main__":
    result = stream_dify_workflow("新能源发展现状")
    print("----------> result <----------")

    # 遍历结果列表，打印最终输出
    for l in result:
        print(l)
