# ================== 说明：cli_demo.py 与 finetune_demo/cli_demo.py 区别与适用场景 ==================
#
# 本 cli_demo.py（在 day35/目录下）:
#   - 适用于原生或官方ChatGLM3模型的本地推理和命令行交互体验。
#   - 重点在于设备适配（支持多种硬件平台，如CPU、NVIDIA/AMD GPU、Apple M1/M2、Intel、摩尔线程等），
#     并提供对环境变量和模型、分词器路径的灵活指定，代码更偏底层和通用，便于初步测试和部署。
#   - 适合刚下载官方模型/权重、希望验证环境和硬件是否兼容模型快速推理，以及用于基础命令行问答交互演示。
#   - 仅依赖 transformers 原生AutoModel, AutoTokenizer接口，不涉及PEFT、LoRA等微调结构判别。
#
# finetune_demo/cli_demo.py（在 day35/ChatGLM3/finetune_demo/ 下）:
#   - 专为finetune_demo模块设计，即微调（如LoRA/PEFT）后的ChatGLM3模型效果验证和命令行交互测试。
#   - 自动判断是否存在PEFT微调结构（adapter_config.json），并能自动处理LoRA等高效参数微调模型的加载。
#   - 模型目录支持微调输出结构（如checkpoint-xxx目录），会正确加载原始权重和adapter融合权重。
#   - 适合模型完成微调后，用于本地实时测试模型在实际QA任务下的答复效果及多轮对话表现。
#   - 更偏向开发人员在finetune/微调流程后的模型效能验证，不关注硬件适配细节，聚焦微调生态。
#
# 总结：本 cli_demo.py 偏重原生、硬件平台适配、模型基础推理的通用性；finetune_demo/cli_demo.py 则更关注微调（如LoRA、Prefix等）后模型的加载与交互验证。两者互补，分别适用于模型初始验收和精调后效果评测。
# ====================================================================================================

# 根据已有规范和实践，通常 finetune_demo/cli_demo.py 用于与微调后的模型做命令行交互推理和效果测试，强调多轮对话和PEFT结构适配。
# 而 finetune_demo/inference_hf.py（如果存在，其命名含义）一般用于如下用途：
#
# 1. 推理脚本化自动批量评测：
#    用于输入一批待测数据（如一个数据集、一个文本列表），让模型批量生成输出（如生成回答或摘要），
#    结果自动保存到文件，便于后续自动评测（如计算BLEU、ROUGE等分数），属于离线批处理推理而非人机交互。
#
# 2. 内嵌于评测/集成流程：
#    通常会内置在pipeline、CI流程，或配合其它评测脚本，实现持续集成环境下的模型效果回归测试。
#
# 3. 系统接口范例：
#    可作为给API、Web、智能体等系统调用的“后端模型预测接口”，
#    封装为函数/类而非命令行交互风格，便于嵌入工程调用。
#
# 通常此类inference脚本更关注“写入读取文件、支持批量任务、结构化I/O、评测兼容性等”，
# 而不专注人机交互流畅体验。因此，cli_demo.py与inference_hf.py协同覆盖了日常测试和大规模推理/评测等常见需求。


import os  # 导入os模块，用于环境变量获取和执行操作系统命令
import platform  # 导入platform模块，用于获取操作系统名称
from transformers import AutoTokenizer, AutoModel  # 加载transformers库中的分词器和模型接口
import torch  # 导入PyTorch库，用于判断硬件和张量运算

# 设定模型路径，优先选择环境变量'MODEL_PATH'，否则采用本地默认路径
MODEL_PATH = os.environ.get('MODEL_PATH', '/root/autodl-tmp/chatglm3-6b')
# 设定分词器路径，优先选择环境变量'TOKENIZER_PATH'，否则与模型路径一致
TOKENIZER_PATH = os.environ.get("TOKENIZER_PATH", MODEL_PATH)
# 判断当前设备是否支持CUDA（NVIDIA/AMD），有则用'cuda'，否则退回'cpu'
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

# ----------------------------------------------------------
#    硬件平台适配说明（仅参考，实际用时请按需解除注释）
#    - Mac (M1/M2): 需安装带Metal支持的PyTorch，设为'mps'
#    - AMD GPU: 需安装ROCm版PyTorch，通常还是设置'cuda'
#    - Intel GPU: 需oneDNN + intel-extension-for-pytorch，设为'xpu'
#    - Moore Threads (MTT S80): 需Musa版PyTorch，设为'musa'
# ----------------------------------------------------------
# 例如M1用户可解除下行注释：
# DEVICE = 'mps'
# 对于Intel GPU，需导入intel扩展
# import intel_extension_for_pytorch as ipex
# DEVICE = 'xpu'
# ----------------------------------------------------------

# 加载分词器（Tokenizer），使用TOKENIZER_PATH路径，并信任远程代码
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH, trust_remote_code=True)

# 根据设备类型加载模型：
if 'cuda' in DEVICE:
    # CUDA类设备（如NVIDIA/AMD显卡）：模型可默认以半精度运行（提升速度和节省显存）
    model = AutoModel.from_pretrained(
        MODEL_PATH, trust_remote_code=True
    ).to(DEVICE).eval()
else:
    # 其他设备（CPU、mps、xpu、musa等）：只能以float精度加载
    model = AutoModel.from_pretrained(
        MODEL_PATH, trust_remote_code=True
    ).float().to(DEVICE).eval()

# 显示一次模型结构信息，便于用户核对模型定义是否加载正确
print(model)
print('-' * 100)

# 获取当前操作系统类型（如Windows、Linux、Darwin等）
os_name = platform.system()
# 设定清屏命令：Windows用'cls'，其他平台统一用'clear'
clear_command = 'cls' if os_name == 'Windows' else 'clear'

# 声明流停止标志位，用于“打断”流式输出（如引入额外中断逻辑可用此flag）
stop_stream = False

# 对话欢迎提示，用于界面友好性指引
welcome_prompt = "欢迎使用 ChatGLM3-6B 模型，输入内容即可进行对话，clear 清空对话历史，stop 终止程序"


def build_prompt(history):
    """
    根据历史对话内容，构建整体对话上下文字符串
    该上下文格式为：
    欢迎语
    用户：xxxx
    ChatGLM3-6B：yyyy
    ...

    Args:
        history (list): 对话历史，为格式为[(用户提问, AI回复), ...] 的列表

    Returns:
        str: 拼接好的完整对话字符串
    """
    prompt = welcome_prompt  # 首先加入欢迎提示语
    # 使用循环，将每一轮历史问答都拼接到prompt字符串中
    for query, response in history:
        prompt += f"\n\n用户：{query}"          # 拼接用户问题
        prompt += f"\n\nChatGLM3-6B：{response}"  # 拼接模型回复
    return prompt

# 解释：关于history无限增长与最大上下文长度限制的关系
#
# 在这里 history 会记录所有对话轮次（每轮为一个 (query, response) 元组的列表），
# 如果用户一直输入，不输入 clear，则 history 会不断变长。
# 但实际上——
# 1. 在调用模型的 stream_chat 或 chat 方法时，真正拼入输入的有效“上下文”，不是简单把所有历史吃进去，
#    而是模型/分词器内部通常会自动裁剪：如果历史累计 token 超过模型最大支持长度（如chatglm3-6b大约8k⾄32k token），
#    只会截取最后几轮对话或最后若干 tokens 进入推理，其它早期内容会被自动丢弃（光存到history没关系）。
# 2. 因此，history 虽然无限增长，但实际模型输入时会被内部流程裁切，保证不会超出最大 context_length 限制。
# 3. 绝大多数ChatGLM系列的chat/stream_chat实现都支持此机制，无需用户手动限制history长度；
#    如果遇到 memory 或效率瓶颈，也可以手动只保留最近N轮history实现"滑动窗口"。
#
# 总结：history的无限增长不影响实际推理的最大上下文长度安全，由模型/接口内部自动处理token截断。


def main():
    """
    命令行主入口。
    - 提示用户输入问题，实时流式输出AI回复
    - 支持clear（清空对话/重置上下文）和stop（退出）指令
    - 会话上下文history与past_key_values用于上下文连续性和推理加速
    """
    # past_key_values用于提升多轮推理效率，history存储全部对话历史
    past_key_values, history = None, []
    global stop_stream  # 声明全局变量stop_stream（如引入自定义中断场景可用）
    # 首次打印欢迎语
    print(welcome_prompt)
    while True:
        # 提示并读取用户输入
        query = input("\n用户：")
        if query.strip() == "stop":
            # 若输入“stop”，则结束程序
            break
        if query.strip() == "clear":
            # 若输入“clear”，则重置历史和缓存，并清屏
            past_key_values, history = None, []
            os.system(clear_command)
            print(welcome_prompt)
            continue
        # 向用户展示模型回复前缀
        print("\nChatGLM：", end="")  # 不换行
        current_length = 0  # 记录已经输出的回复长度（用于流式增量输出）
        # 调用模型的stream_chat接口，实现边生成边输出（支持多轮对话与高效推理）
        for response, history, past_key_values in model.stream_chat(
            tokenizer,
            query,
            history=history,                # 传入历史轮次
            top_p=1,                        # 控制生成的多样性
            temperature=0.01,               # 控制生成的随机性
            past_key_values=past_key_values, # 复用历史KV缓存提升效率
            return_past_key_values=True     # 要求返回KV用于下轮
        ):
            if stop_stream:
                # 若stop_stream被外部置True，则中断此次流输出（片段可用于扩展键盘中止等功能）
                stop_stream = False
                break
            else:
                # 流式增量输出最新生成的内容
                print(response[current_length:], end="", flush=True)
                current_length = len(response)  # 更新已输出长度
        print("")  # 单轮回复结束后打印换行


if __name__ == "__main__":
    # 只有直接运行文件时才调用main()
    main()
