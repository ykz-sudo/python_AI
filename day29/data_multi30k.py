# Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os  # 用于文件与目录操作
from tqdm import tqdm  # 可选，用于显示进度条（当前未实际使用）
import xml.etree.ElementTree as ET  # 可选，处理XML数据（当前未实际使用）
from sacremoses import MosesTokenizer  # 导入Moses分词器，用于对文本进行分词处理
from pathlib import Path  # 提供面向对象的路径接口
import argparse  # 处理命令行参数解析

def moses_cut(in_file, out_file, lang):
    """
    对输入文本文件进行分词处理，并将结果写入输出文件。
    每行一个句子，经过分词后转为小写，换行保存。

    参数:
        in_file (str or Path): 输入文件路径，要求为每行一句话。
        out_file (str or Path): 输出文件路径。
        lang (str): 指定的语言代码（如 'en' 或 'de'），用于初始化Moses分词器。
    """
    mt = MosesTokenizer(lang=lang)  # 按语言初始化MosesTokenizer分词器
    out_f = open(out_file, "w", encoding="utf8")  # 以utf8写模式打开输出文件
    with open(in_file, "r", encoding="utf8") as f:  # 读模式打开源文本文件
        for line in f.readlines():  # 逐行读取
            line = line.strip()  # 去掉多余空白符
            if not line:
                # 如果是空行则跳过
                continue
            cut_line = mt.tokenize(line, return_str=True)  # 分词，按空格拼接
            out_f.write(cut_line.lower() + "\n")  # 转小写并写入输出文件（每行一句）
    out_f.close()  # 关闭输出文件资源

if __name__ == "__main__":
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser()  # 初始化参数解析器
    # 添加参数 --pair_dir 或 -p：
    # 用法示例：
    #   python data_multi30k.py --pair_dir data/raw ...
    # 表示原版双语配对数据所在的目录（如 data/raw），该目录下应该包含 train.de, train.en, val.de, val.en, test.de, test.en 等文件。
    parser.add_argument(
        "-p",
        "--pair_dir",
        default=None,
        type=str,
        help=(
            "The directory containing parallel data files (e.g., train.de, train.en, val.de, val.en, test.de, test.en). "
            "Example: --pair_dir data/raw"
        ),  # 语言对原数据所在目录，见上述用法解释
    )
    parser.add_argument(
        "-d",
        "--dest_dir",
        default=None,
        type=str,
        help="The destination directory to save processed train, dev and test file.",  # 处理好结果输出目录
    )
    parser.add_argument("--src_lang", default="de", type=str, help="source language")  # 源语言代码
    parser.add_argument("--trg_lang", default="en", type=str, help="target language")  # 目标语言代码

    # args 是通过 argparse.ArgumentParser().parse_args() 得到的命名空间对象（Namespace 类型），
    # 其各个属性（如 args.pair_dir, args.dest_dir, args.src_lang, args.trg_lang）对应命令行参数值。
    # 用法示例：
    #   args.pair_dir      # 获取 --pair_dir 参数
    #   args.dest_dir      # 获取 --dest_dir 参数
    #   args.src_lang      # 获取 --src_lang 参数
    #   args.trg_lang      # 获取 --trg_lang 参数

    args = parser.parse_args()  # 解析命令行参数为args对象

    # 检查源语言数据目录是否指定，否则报错
    if not args.pair_dir:
        raise ValueError("Please specify --pair_dir")

    # 若目标输出目录不存在，则新建之
    if not os.path.exists(args.dest_dir):
        os.makedirs(args.dest_dir)
    
    # 将路径处理为Path对象，便于拼接与操作
    local_data_path = Path(args.pair_dir)  # 原始语言文件目录，如 data/raw
    data_dir = Path(args.dest_dir)  # 输出分词文件目录，如 data/preproc

    # 依次处理train/val/test三种数据模式
    for mode in ["train", "val", "test"]:
        # 1. 分词处理源语言文件
        moses_cut(
            local_data_path / f"{mode}.{args.src_lang}",  # 输入：如 data/raw/train.de
            data_dir / f"{mode}_src.cut.txt",             # 输出：如 data/preproc/train_src.cut.txt
            lang=args.src_lang,                           # 源语言代码
        )
        print(f"[{mode}] 源语言文本分词完成")
        # 2. 分词处理目标语言文件
        moses_cut(
            local_data_path / f"{mode}.{args.trg_lang}",  # 输入：如 data/raw/train.en
            data_dir / f"{mode}_trg.cut.txt",             # 输出：如 data/preproc/train_trg.cut.txt
            lang=args.trg_lang,                           # 目标语言代码
        )
        print(f"[{mode}] 目标语言文本分词完成")
        # 分别提示本轮数据处理已完成
