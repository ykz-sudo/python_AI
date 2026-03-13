"""
GLM-4原始基座模型评估脚本
手动对数据集样本进行推理，计算BLEU-4、ROUGE-1、ROUGE-2、ROUGE-L评估指标

用法说明：
- 设置MODEL_PATH环境变量或修改脚本中的默认路径（指向原始基座模型，如THUDM/glm-4-9b-chat）
- 设置EVAL_DATA_PATH指向评估数据集（jsonl格式）
- 运行脚本进行推理和评估

注意事项:
- 本脚本专门用于评估**原始基座模型**（未微调的预训练模型）
- MODEL_PATH可以是HuggingFace Hub上的模型ID（如THUDM/glm-4-9b-chat）或本地路径
- 推理结果会保存到指定文件，便于后续分析
- 如需评估微调后的模型，请使用 eval.py
"""

import os
import json
import torch
from pathlib import Path
from typing import Union, List, Dict, Any
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizer,
    PreTrainedTokenizerFast,
    StoppingCriteria,
    StoppingCriteriaList,
)
from datasets import load_dataset  # HuggingFace datasets库，用于加载数据集

# 评估指标计算库
try:
    from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
    import nltk
    # 下载必要的NLTK数据
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
except ImportError:
    print("警告: 未安装nltk，BLEU指标将无法计算。请运行: pip install nltk")
    sentence_bleu = None

try:
    from rouge_score import rouge_scorer
except ImportError:
    print("警告: 未安装rouge-score，ROUGE指标将无法计算。请运行: pip install rouge-score")
    rouge_scorer = None

# 类型别名，提升类型注解可读性
ModelType = PreTrainedModel
TokenizerType = Union[PreTrainedTokenizer, PreTrainedTokenizerFast]

# 设置模型检查点路径，优先取环境变量，否则取默认路径（原始基座模型）
# 默认使用HuggingFace Hub上的GLM-4-9B-Chat模型
MODEL_PATH = os.environ.get('MODEL_PATH', 'THUDM/glm-4-9b-chat')
# 设置评估数据集路径
EVAL_DATA_PATH = os.environ.get('EVAL_DATA_PATH', '/root/GLM-4/finetune_demo/data/dev.jsonl')
# 设置结果保存路径
RESULTS_SAVE_PATH = os.environ.get('RESULTS_SAVE_PATH', '/root/evaluation_results_base.json')


def load_model_and_tokenizer(
        model_dir: Union[str, Path], trust_remote_code: bool = True
) -> tuple[ModelType, TokenizerType]:
    """
    加载原始基座模型（未微调）的GLM-4 CausalLM模型及Tokenizer
    Args:
        model_dir: 模型所在路径（可为本地路径或HuggingFace Hub模型ID）
        trust_remote_code: 是否信任远程自定义代码
    Returns:
        (模型实例, 分词器实例) -> tuple[ModelType, TokenizerType]
    """
    model_dir_str = str(model_dir)
    
    # 检查是否是本地路径
    model_dir_path = Path(model_dir).expanduser()
    is_local_path = model_dir_path.exists() and model_dir_path.is_dir()
    
    if is_local_path:
        # 本地路径，解析为绝对路径
        model_dir_path = model_dir_path.resolve()
        model_dir_str = str(model_dir_path)
        
        # 检查是否存在config.json，确认是有效的模型目录
        config_path = model_dir_path / 'config.json'
        if not config_path.exists():
            raise ValueError(f"模型目录无效，未找到config.json: {model_dir_path}")
    
    # 加载原始基座模型（不支持PEFT，直接加载）
    try:
        model = AutoModelForCausalLM.from_pretrained(
            model_dir_str, 
            trust_remote_code=trust_remote_code, 
            device_map='auto'
        )
    except (OSError, ValueError) as e:
        # 如果是本地路径且失败，尝试使用local_files_only
        if is_local_path:
            print(f"警告: 直接加载失败，尝试使用local_files_only: {e}")
            try:
                model = AutoModelForCausalLM.from_pretrained(
                    model_dir_str, 
                    trust_remote_code=trust_remote_code, 
                    device_map='auto',
                    local_files_only=True
                )
            except Exception as e2:
                raise RuntimeError(f"无法加载模型，尝试了多种方法均失败。最后错误: {e2}")
        else:
            raise
    
    # 加载tokenizer
    try:
        tokenizer = AutoTokenizer.from_pretrained(
            model_dir_str, 
            trust_remote_code=trust_remote_code, 
            encode_special_tokens=True, 
            use_fast=False
        )
    except (OSError, ValueError) as e:
        # 如果是本地路径且失败，尝试使用local_files_only
        if is_local_path:
            print(f"警告: tokenizer加载失败，尝试使用local_files_only: {e}")
            tokenizer = AutoTokenizer.from_pretrained(
                model_dir_str,
                trust_remote_code=trust_remote_code, 
                encode_special_tokens=True, 
                use_fast=False,
                local_files_only=True
            )
        else:
            raise
    
    model.eval()  # 设置为评估模式，不计算梯度
    return model, tokenizer


class StopOnTokens(StoppingCriteria):
    """
    自定义停止准则，当生成序列的最后token属于模型eos_token_id时触发终止
    """
    def __init__(self, eos_token_ids: List[int]):
        """
        Args:
            eos_token_ids: 结束token ID列表
        """
        self.eos_token_ids = eos_token_ids
    
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        """
        检查是否应该停止生成
        Args:
            input_ids: 当前生成的token序列
            scores: 模型输出的分数
        Returns:
            bool: 如果应该停止则返回True
        """
        for stop_id in self.eos_token_ids:
            if input_ids[0][-1] == stop_id:      # 当前批次最后生成token为stop id则终止
                return True
        return False


def generate_response(
        model: ModelType,
        tokenizer: TokenizerType,
        user_input: str,
        max_length: int = 8192,
        top_p: float = 0.7,
        temperature: float = 0.9,
        repetition_penalty: float = 1.2,
) -> str:
    """
    基于模型与Tokenizer完成一个对话回合，生成模型回复
    Args:
        model: 模型实例
        tokenizer: 分词器实例
        user_input: 用户输入文本
        max_length: 最大生成长度（token数）
        top_p: top-p采样阈值
        temperature: 温度采样参数
        repetition_penalty: 重复惩罚系数
    Returns:
        str: 模型生成的回复内容
    """
    # 构造ChatML消息列表
    messages = [{"role": "user", "content": user_input}]
    
    # 应用聊天模板并转换为tensor
    model_inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_tensors="pt"
    ).to(model.device)
    
    # 获取eos_token_id
    eos_token_ids = model.config.eos_token_id
    if isinstance(eos_token_ids, int):
        eos_token_ids = [eos_token_ids]
    
    # 创建停止准则
    stop = StopOnTokens(eos_token_ids)
    
    # 构造生成参数
    generate_kwargs = {
        "input_ids": model_inputs,
        "max_new_tokens": max_length,
        "do_sample": True,
        "top_p": top_p,
        "temperature": temperature,
        "stopping_criteria": StoppingCriteriaList([stop]),
        "repetition_penalty": repetition_penalty,
        "eos_token_id": eos_token_ids,
        "pad_token_id": tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id,
    }
    
    # 生成回复
    with torch.no_grad():  # 推理时不计算梯度，节省显存
        outputs = model.generate(**generate_kwargs)
    
    # 解码生成的token（只解码新生成的部分）
    generated_ids = outputs[0][model_inputs.shape[1]:]  # 只取新生成的token
    response = tokenizer.decode(generated_ids, skip_special_tokens=True)
    
    return response.strip()  # 去除首尾空白


def load_eval_dataset(data_path: str) -> List[Dict[str, Any]]:
    """
    加载评估数据集（jsonl格式）
    Args:
        data_path: 数据集文件路径
    Returns:
        List[Dict[str, Any]]: 数据集样本列表，每个样本包含messages字段
    """
    data_path = Path(data_path)
    if not data_path.exists():
        raise FileNotFoundError(f"数据集文件不存在: {data_path}")
    
    # 使用datasets库加载jsonl文件
    dataset = load_dataset('json', data_files=str(data_path), split='train')
    
    # 转换为列表格式
    samples = []
    for item in dataset:
        samples.append(item)
    
    return samples


def extract_user_and_assistant(messages: List[Dict[str, str]]) -> tuple[str, str]:
    """
    从messages列表中提取用户输入和助手回复
    Args:
        messages: 消息列表，每个消息包含role和content字段
    Returns:
        tuple[str, str]: (用户输入, 助手回复)
    """
    user_input = ""
    assistant_output = ""
    
    for msg in messages:
        role = msg.get('role', '')
        content = msg.get('content', '')
        if role == 'user':
            user_input = content
        elif role == 'assistant':
            assistant_output = content
    
    return user_input, assistant_output


def calculate_bleu4(reference: str, prediction: str) -> float:
    """
    计算BLEU-4分数
    Args:
        reference: 参考文本（真实答案）
        prediction: 预测文本（模型生成）
    Returns:
        float: BLEU-4分数，范围0-1
    """
    if sentence_bleu is None:
        return 0.0
    
    # 将文本分词（中文按字符分词，英文按空格分词）
    # 对于中文，按字符分割；对于英文，按单词分割
    import re
    # 判断是否包含中文字符
    has_chinese = bool(re.search(r'[\u4e00-\u9fff]', reference + prediction))
    
    if has_chinese:
        # 中文按字符分割
        ref_tokens = list(reference.replace(' ', ''))  # 移除空格后按字符分割
        pred_tokens = list(prediction.replace(' ', ''))
    else:
        # 英文按单词分割
        ref_tokens = reference.split()
        pred_tokens = prediction.split()
    
    # 如果预测为空，返回0
    if not pred_tokens:
        return 0.0
    
    # 使用平滑函数避免0分
    smoothing = SmoothingFunction().method1
    score = sentence_bleu([ref_tokens], pred_tokens, weights=(0.25, 0.25, 0.25, 0.25), smoothing_function=smoothing)
    
    return score


def calculate_rouge_scores(reference: str, prediction: str) -> Dict[str, float]:
    """
    计算ROUGE-1、ROUGE-2、ROUGE-L分数
    Args:
        reference: 参考文本（真实答案）
        prediction: 预测文本（模型生成）
    Returns:
        Dict[str, float]: 包含rouge1、rouge2、rougel的字典，每个值范围0-1
    """
    if rouge_scorer is None:
        return {'rouge1': 0.0, 'rouge2': 0.0, 'rougel': 0.0}
    
    # 检查输入是否为空
    if not reference or not prediction:
        return {'rouge1': 0.0, 'rouge2': 0.0, 'rougel': 0.0}
    
    try:
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=False)
        scores = scorer.score(reference, prediction)
        
        return {
            'rouge1': scores['rouge1'].fmeasure,  # ROUGE-1 F1分数
            'rouge2': scores['rouge2'].fmeasure,  # ROUGE-2 F1分数
            'rougel': scores['rougeL'].fmeasure,  # ROUGE-L F1分数
        }
    except Exception as e:
        # 如果计算失败，打印错误信息并返回0
        print(f"警告: ROUGE计算失败: {e}")
        return {'rouge1': 0.0, 'rouge2': 0.0, 'rougel': 0.0}


def evaluate_model(
        model: ModelType,
        tokenizer: TokenizerType,
        eval_samples: List[Dict[str, Any]],
        save_path: str = None,
) -> Dict[str, float]:
    """
    对模型进行评估，计算各项指标
    Args:
        model: 模型实例
        tokenizer: 分词器实例
        eval_samples: 评估样本列表
        save_path: 结果保存路径（可选）
    Returns:
        Dict[str, float]: 包含各项评估指标的字典
    """
    print(f"开始评估，共 {len(eval_samples)} 个样本...")
    
    references = []  # 参考答案列表
    predictions = []  # 模型预测列表
    results = []     # 详细结果列表，用于保存
    
    # 对每个样本进行推理
    for idx, sample in enumerate(eval_samples):
        if idx % 10 == 0:
            print(f"处理进度: {idx}/{len(eval_samples)}")
        
        messages = sample.get('messages', [])
        user_input, reference = extract_user_and_assistant(messages)
        
        if not user_input or not reference:
            print(f"警告: 样本 {idx} 缺少user或assistant消息，跳过")
            continue
        
        # 生成模型预测
        try:
            prediction = generate_response(model, tokenizer, user_input)
        except Exception as e:
            print(f"错误: 样本 {idx} 推理失败: {e}")
            prediction = ""
        
        references.append(reference)
        predictions.append(prediction)
        
        # 保存详细结果
        results.append({
            'index': idx,
            'user_input': user_input,
            'reference': reference,
            'prediction': prediction,
        })
    
    print(f"推理完成，开始计算评估指标...")
    
    # 检查rouge-score库是否可用
    if rouge_scorer is None:
        print("=" * 50)
        print("警告: rouge-score库未安装，ROUGE指标将无法计算！")
        print("请运行以下命令安装: pip install rouge-score")
        print("=" * 50)
    else:
        print("ROUGE库已加载，开始计算ROUGE指标...")
    
    # 检查预测结果是否为空
    empty_predictions = sum(1 for p in predictions if not p.strip())
    if empty_predictions > 0:
        print(f"警告: 有 {empty_predictions} 个预测结果为空")
    
    # 计算各项指标
    bleu4_scores = []
    rouge1_scores = []
    rouge2_scores = []
    rougel_scores = []
    
    for idx, (ref, pred) in enumerate(zip(references, predictions)):
        # 计算BLEU-4
        bleu4 = calculate_bleu4(ref, pred)
        bleu4_scores.append(bleu4)
        
        # 计算ROUGE分数
        rouge_scores = calculate_rouge_scores(ref, pred)
        rouge1_scores.append(rouge_scores['rouge1'])
        rouge2_scores.append(rouge_scores['rouge2'])
        rougel_scores.append(rouge_scores['rougel'])
        
        # 打印前几个样本的调试信息
        if idx < 3:
            print(f"\n样本 {idx} 调试信息:")
            print(f"  参考文本长度: {len(ref)}")
            print(f"  预测文本长度: {len(pred)}")
            print(f"  ROUGE-1: {rouge_scores['rouge1']:.4f}")
            print(f"  ROUGE-2: {rouge_scores['rouge2']:.4f}")
            print(f"  ROUGE-L: {rouge_scores['rougel']:.4f}")
    
    # 计算平均分数
    avg_bleu4 = sum(bleu4_scores) / len(bleu4_scores) if bleu4_scores else 0.0
    avg_rouge1 = sum(rouge1_scores) / len(rouge1_scores) if rouge1_scores else 0.0
    avg_rouge2 = sum(rouge2_scores) / len(rouge2_scores) if rouge2_scores else 0.0
    avg_rougel = sum(rougel_scores) / len(rougel_scores) if rougel_scores else 0.0
    
    # 汇总结果
    metrics = {
        'bleu4': avg_bleu4,
        'rouge1': avg_rouge1,
        'rouge2': avg_rouge2,
        'rougel': avg_rougel,
    }
    
    # 保存详细结果
    if save_path:
        output_data = {
            'metrics': metrics,
            'detailed_results': results,
        }
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"评估结果已保存到: {save_path}")
    
    return metrics


def main():
    """
    主函数：加载模型、数据集，执行评估
    """
    print("=" * 50)
    print("GLM-4 原始基座模型评估脚本")
    print("=" * 50)
    
    # 检查依赖库
    print("\n检查依赖库状态:")
    if rouge_scorer is None:
        print("  ❌ rouge-score: 未安装")
        print("     请运行: pip install rouge-score")
    else:
        print("  ✅ rouge-score: 已安装")
        # 测试ROUGE计算是否正常工作
        try:
            test_scorer = rouge_scorer.RougeScorer(['rouge1'], use_stemmer=False)
            test_scores = test_scorer.score("这是一个测试", "这是一个测试")
            if test_scores['rouge1'].fmeasure > 0:
                print("     测试: ROUGE计算功能正常")
            else:
                print("     警告: ROUGE计算返回0，可能存在问题")
        except Exception as e:
            print(f"     警告: ROUGE测试失败: {e}")
    
    if sentence_bleu is None:
        print("  ❌ nltk: 未安装")
        print("     请运行: pip install nltk")
    else:
        print("  ✅ nltk: 已安装")
    print()
    
    # 加载模型和分词器
    print(f"\n正在加载原始基座模型: {MODEL_PATH}")
    model, tokenizer = load_model_and_tokenizer(MODEL_PATH, trust_remote_code=True)
    print("模型加载完成")
    
    # 加载评估数据集
    print(f"\n正在加载评估数据集: {EVAL_DATA_PATH}")
    eval_samples = load_eval_dataset(EVAL_DATA_PATH)
    print(f"数据集加载完成，共 {len(eval_samples)} 个样本")
    
    # 执行评估
    print("\n开始评估...")
    metrics = evaluate_model(model, tokenizer, eval_samples, save_path=RESULTS_SAVE_PATH)
    
    # 打印评估结果
    print("\n" + "=" * 50)
    print("评估结果:")
    print("=" * 50)
    print(f"BLEU-4:  {metrics['bleu4']:.4f}")
    print(f"ROUGE-1: {metrics['rouge1']:.4f}")
    print(f"ROUGE-2: {metrics['rouge2']:.4f}")
    print(f"ROUGE-L: {metrics['rougel']:.4f}")
    print("=" * 50)


if __name__ == '__main__':
    main()

