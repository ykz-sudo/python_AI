import json

def process_jsonl_to_conversations(input_file, output_file):
    """
    将 JSONL 文件中的每个样本转换为对话格式
    
    参数说明:
        input_file: 输入的 JSONL 文件路径，每行为一个字典，通常含有 input/output 字段
        output_file: 输出的 JSONL 文件路径，每行为一个新的 conversations 格式字典

    处理流程:
        1. 逐行读取原始 JSONL 文件，对每一行字符串去除首尾空白再解析为 JSON 数据结构（dict）。
        2. 分别提取每条数据中的 'input' 字段（视为 user 提问）和 'output' 字段（视为 assistant 回复）。
        3. 组装为如下格式：
             {
                 "conversations": [
                     {"role": "user", "content": ...},
                     {"role": "assistant", "content": ...}
                 ]
             }
        4. 按行写入到新的 JSONL 输出文件，确保每行一个 JSON 对象，且不转义中文。
        5. 对于解析失败（JSON格式错）或其他异常，打印明确信息（包含行号），继续处理下一行。
        6. 结束时输出总处理数据量。

    异常说明:
        - 当输入文件中某行不是合法 JSON 或格式错误，会被安全捕获并显示报错行数与原因，不影响后序处理。
    """
    # 打开输入文件进行读取，打开输出文件进行写入，均指定 utf-8 编码保证中文兼容
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:
        
        # 逐行读取，line_num 从 1 开始方便异常时定位
        for line_num, line in enumerate(f_in, 1):
            try:
                # 去除行首尾的空白，并尝试反序列化为 Python 字典
                data = json.loads(line.strip())
                
                # 从原始字典安全获取 'input'（用户提问内容）、'output'（助手回复内容）
                user_content = data.get('input', '')           # 若无 input 字段则为空串
                assistant_content = data.get('output', '')     # 若无 output 字段则为空串
                
                # 构造目标格式 conversations（一个 user 轮和一个 assistant 轮）
                result = {
                    "conversations": [
                        {
                            "role": "user",            # 标记角色为用户
                            "content": user_content    # 用户的内容
                        },
                        {
                            "role": "assistant",       # 标记角色为助手
                            "content": assistant_content # 助手的内容
                        }
                    ]
                }
                
                # 将结果字典序列化为 JSON 字符串，ensure_ascii=False 确保中文正常输出
                # 每一个 JSON 对象单独占据一行，符合 JSONL 规范
                f_out.write(json.dumps(result, ensure_ascii=False) + '\n')
                
            except json.JSONDecodeError as e:
                # 捕捉 JSON 解析错误，输出当前行号和异常信息，继续处理下一行
                print(f"第 {line_num} 行 JSON 解析错误: {e}")
                continue
            except Exception as e:
                # 其它任意异常都安全捕捉，输出当前行号和具体错误
                print(f"第 {line_num} 行处理错误: {e}")
                continue
    
    # 当 with 块退出，即全部处理完毕，打印总共处理的行数
    print(f"处理完成！已处理 {line_num} 行数据")

if __name__ == "__main__":
    # 指定输入输出文件名（可按需修改）
    input_file = "DISC-Law-SFT-Triplet-released.jsonl"
    output_file = "DISC-Law-SFT-Triplet-conversations.jsonl"
    
    # 调用数据处理函数开始处理
    process_jsonl_to_conversations(input_file, output_file)

