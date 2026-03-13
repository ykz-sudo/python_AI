"""
本脚本创建了一个基于transformers后端的glm-4-9b模型CLI演示，
支持LoRA/PEFT参数微调加载，允许通过命令行或Web API与模型交互。

用法说明：
- 启动脚本，得到CLI或API服务。
- 输入问题与模型对话，获得模型回复。

注意事项:
- 支持将Markdown格式输出转换为纯文本，确保在CLI端友好显示格式化内容。
- 如需使用flash attention，请提前安装flash-attn，并在模型加载处增加 attn_implementation="flash_attention_2"。

"""

import os
import torch
from threading import Thread               # 用于异步生成模型输出，提高交互流畅性
from typing import Union
from pathlib import Path                   # 路径处理工具
from peft import AutoPeftModelForCausalLM, PeftModelForCausalLM    # PEFT参数高效微调相关模型接口
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizer,
    PreTrainedTokenizerFast,
    StoppingCriteria,
    StoppingCriteriaList,
    TextIteratorStreamer                  # 用于流式输出生成内容
)
import tornado.web                        # Tornado用于构建Web API服务
import tornado.ioloop
from tornado.web import RequestHandler    # HTTP请求处理基类

# 类型别名，提升类型注解可读性
ModelType = Union[PreTrainedModel, PeftModelForCausalLM]
TokenizerType = Union[PreTrainedTokenizer, PreTrainedTokenizerFast]

# 设置模型检查点路径，优先取环境变量，否则取默认路径
MODEL_PATH = os.environ.get('MODEL_PATH', '/root/GLM-4/finetune_demo/output/模型保存点')


def load_model_and_tokenizer(
        model_dir: Union[str, Path], trust_remote_code: bool = True
) -> tuple[ModelType, TokenizerType]:
    """
    加载支持PEFT微调（如LoRA适配器）或常规SFT微调的GLM-4 CausalLM模型及Tokenizer
    Args:
        model_dir: 模型所在路径（可为本地或远程）
        trust_remote_code: 是否信任远程自定义代码
    Returns:
        (模型实例, 分词器实例)
    """
    model_dir = Path(model_dir).expanduser().resolve()   # 解析出绝对路径
    if (model_dir / 'adapter_config.json').exists():
        # 存在adapter_config.json即为PEFT模型（如LoRA结构的微调模型）
        model = AutoPeftModelForCausalLM.from_pretrained(
            model_dir, trust_remote_code=trust_remote_code, device_map='auto')
        # PEFT模型的tokenizer需要指向底座模型（基础模型）目录
        # 取LoRA等PEFT适配器下基础模型（底座模型）路径，作为分词器加载路径
        
        # INSERT_YOUR_CODE
        # 为什么要是base model的路径
        # LoRA等PEFT微调方法只训练和保存了部分adapter权重，分词器相关的文件并不会被包含在PEFT微调输出目录中。
        # 因此，解码/分词器对象应始终从基础模型(base model)的目录加载，避免由于PEFT adapter目录中无分词器配置文件而导致出错。
        # 这保证了分词器的词表、特殊token等信息与底座模型完全一致，不会出现不兼容问题。
        
        # INSERT_YOUR_CODE
        # 解释：peft_config['default'].base_model_name_or_path
        # peft_config是PEFT模型的配置字典（或者对象），包含了adapter相关的底座模型信息
        # 'default'是适配器名称（通常LoRA等adapter会用'default'作为主adapter键名）
        # base_model_name_or_path字段记录了本次PEFT微调所对应的基础（底座）模型的huggingface名称或本地路径
        # 例子: 如果你用THUDM/glm-4-9b进行LoRA微调，那么
        # peft_config['default'].base_model_name_or_path == 'THUDM/glm-4-9b'
        # 这样可以确保tokenizer始终指向GLM-4-9b原始模型目录/名称
        tokenizer_dir = model.peft_config['default'].base_model_name_or_path
    else:
        # 普通SFT模型（全量微调），直接加载
        model = AutoModelForCausalLM.from_pretrained(
            model_dir, trust_remote_code=trust_remote_code, device_map='auto')
        tokenizer_dir = model_dir
    # 加载tokenizer。关闭use_fast以兼容chatglm特殊分词器，encode_special_tokens开启特殊token编码
    tokenizer = AutoTokenizer.from_pretrained(
        tokenizer_dir, trust_remote_code=trust_remote_code, encode_special_tokens=True, use_fast=False
    )
    return model, tokenizer

# 加载模型和分词器，为全局唯一
model, tokenizer = load_model_and_tokenizer(MODEL_PATH, trust_remote_code=True)

class StopOnTokens(StoppingCriteria):
    """
    自定义停止准则，当生成序列的最后token属于模型eos_token_id时触发终止
    """
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        stop_ids = model.config.eos_token_id     # 模型eos_token_id一般为一个或多个
        for stop_id in stop_ids:
            if input_ids[0][-1] == stop_id:      # 当前批次最后生成token为stop id则终止
                return True
        return False

def chatbot_api(infos):
    """
    chatbot_api的作用：
    该函数接收用户输入（infos），基于全局加载的模型与Tokenizer，完成一次对话回复流程。
    适用于命令行或者REST API等场景，能够流式生成模型回复。

    实现流程：
    1. 接收用户输入，将其添加到history用于后续消息构建（这里只保留单轮历史）。
    2. 按照ChatML结构拼接消息，并调用Tokenizer将消息转为模型输入。
    3. 基于指定的生成参数和自定义停止准则，异步调用模型的.generate方法进行文本生成，同时通过streamer流式输出新token。
    4. 每生成一个新token，实时累加到history并打印输出（适合命令行打字效果等场景）。
    5. 最终返回本轮模型的完整回复内容（去除首尾空白）。

    Args:
        infos (str): 用户输入字符串
    Returns:
        str: 本轮模型回复
    """
    history = []              # 存储单轮历史
    max_length = 8192         # 最大生成长度
    top_p = 0.7               # top-p采样，提升生成多样性
    temperature = 0.9         # 温度采样，控制生成随机度
    stop = StopOnTokens()     # 停止准则

    print("Welcome to the GLM-4-9B CLI chat. Type your messages below.")

    user_input = infos
    # history存入本输入（第一项为用户输入，第二项预留模型回复）
    history.append([user_input, ""])

    # 构造ChatML格式的消息，仅用本轮输入
    messages = []
    for idx, (user_msg, model_msg) in enumerate(history):
        if idx == len(history) - 1 and not model_msg:
            messages.append({"role": "user", "content": user_msg})
            break
        if user_msg:
            messages.append({"role": "user", "content": user_msg})
        if model_msg:
            messages.append({"role": "assistant", "content": model_msg})

    # 应用chat模板并编码为输入张量
    model_inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_tensors="pt"
    ).to(model.device)

    # 创建流式文本生成器
    streamer = TextIteratorStreamer(
        tokenizer=tokenizer,
        timeout=60,
        skip_prompt=True,
        skip_special_tokens=True
    )
    # 拼装生成参数
    generate_kwargs = {
        "input_ids": model_inputs,
        "streamer": streamer,
        "max_new_tokens": max_length,
        "do_sample": True,
        "top_p": top_p,
        "temperature": temperature,
        "stopping_criteria": StoppingCriteriaList([stop]),
        "repetition_penalty": 1.2,
        "eos_token_id": model.config.eos_token_id,
    }
    # 启动生成线程，生成reply
    # 这是Python的threading.Thread用法，表示在新线程中异步调用模型的generate方法
    # 这样主线程可以实时处理streamer流式输出，实现流畅的对话体验

    # 下面这两行代码用来启动一个新线程，在新线程中运行模型的generate函数。
    # 这样做的目的是：模型生成回答时可能会比较慢，如果直接在主线程（即主程序）中调用，主线程会被阻塞，导致无法实时显示生成的内容或响应其它操作。
    # 使用Thread可以让generate过程在后台运行，主线程则可以一边不断读取streamer流出的新token，一边实时显示给用户，实现流畅的对话体验（像“打字机”效果）。
    
    # INSERT_YOUR_CODE
    # 是的，generate是transformers库（包括GLM4模型的transformers分支）提供的生成文本（文本续写、对话等）接口方法。
    # 它会根据输入的input_ids自动触发模型的光标预测、采样/解码等流程，生成下一个token并不断向后预测直到满足停止准则。
    # GLM-4的官方模型也是遵循transformers框架标准API（如generate），因此可以用Thread(target=model.generate, ...)方式调用流式生成。
    t = Thread(target=model.generate, kwargs=generate_kwargs)
    t.start()
    print("GLM-4:", end="", flush=True)
    for new_token in streamer:
        if new_token:
            print(new_token, end="", flush=True)
            history[-1][1] += new_token   # 回复累积

    history[-1][1] = history[-1][1].strip()    # 去除空白
    return history[-1][1]



# ========== Tornado Web服务相关 ==========
class BaseHandler(RequestHandler):
    """基础请求处理器，统一设置CORS以支持跨域访问（AJAX等）"""

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')        # 允许所有来源跨域
        self.set_header('Access-Control-Allow-Methods', 'POST, GET')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')
        # self.set_header('Content-type', 'application/json')    # 如需指定返回格式可开启

class IndexHandler(BaseHandler):
    """
    IndexHandler用于处理/api/chatbot的GET请求。

    实际用途为：当前端（如网页、前端应用、Postman等）通过HTTP GET方式访问
    /api/chatbot，并传递参数infos（即用户输入的问题）时，
    本类负责解析请求、调用chatbot_api获取模型回复，并将结果返回给前端页面。

    主要流程为：
    - 从URL中获取"infos"参数（即用户输入内容）
    - 调用chatbot_api(infos=...)完成对GLM-4的推理
    - 将GLM-4的回复通过HTTP响应体write回前端
    - 如出错则返回"服务器内部错误"
    """
    def get(self):
        # 获取前端传来的用户输入内容（?infos=xxx），如无则返回400
        infos = self.get_query_argument("infos", default=None)
        if infos is None:
            self.set_status(400)
            self.write("缺少infos参数")
            return
        print("Q:", infos)
        # 捕获chatbot调用的异常，保证后端服务稳定
        try:
            result = chatbot_api(infos=infos)  # 推理获得回复
        except Exception as e:
            print("推理异常:", e)
            self.set_status(500)
            self.write("服务器内部错误")
            return
        reply = "".join(result) if isinstance(result, (list, tuple)) else str(result)
        print("A:", reply)
        self.write(reply)  # 返回推理结果到前端

if __name__ == '__main__':
    # 创建Tornado应用实例，并注册路由
    # 这段代码的作用是创建Tornado Web应用，并将特定的URL路由（如/api/chatbot）与处理类(IndexHandler)绑定，从而使Web服务器能够监听、接收和处理前端页面或其他客户端发来的HTTP请求。
    # 原理：tornado.web.Application([]) 用于配置路由表，将URL与对应的处理类匹配；当有用户访问 /api/chatbot 时，会由IndexHandler来处理请求，实现和大模型后端的对接。
    app = tornado.web.Application([
        (r'/api/chatbot', IndexHandler)      # 聊天API接口绑定
    ])
    # 绑定服务端口6006
    app.listen(6006)
    # 启动Tornado事件循环，开始提供web服务
    tornado.ioloop.IOLoop.current().start()