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

import os  # 用于文件系统操作，如目录检测和创建
from tqdm import tqdm  # 用于显示进度条（此脚本中未用到，可根据需要删除）
import xml.etree.ElementTree as ET  # 用于XML处理（此脚本中未用到，可根据需要删除）
from sacremoses import MosesTokenizer  # 引入Moses分词器
from pathlib import Path  # 提供面向对象风格的路径操作
import argparse  # 用于命令行参数解析

def moses_cut(in_file, out_file, lang):
    """
    对指定文本文件进行分词处理，并将分词结果输出到目标文件。

    Args:
        in_file (str or Path): 输入文件路径，每行一个待分词句子。
        out_file (str or Path): 输出分词后文件路径。
        lang (str): 语言代码（如'en', 'de'），用于初始化分词器。
    """
    mt = MosesTokenizer(lang=lang)  # 初始化Moses分词器，指定语言
    out_f = open(out_file, "w", encoding="utf8")  # 以utf8写入模式打开输出文件
    with open(in_file, "r", encoding="utf8") as f:  # 以utf8读取模式打开输入文件
        for line in f.readlines():  # 逐行读取输入文件内容
            line = line.strip()  # 去除首尾空白字符
            if not line:
                # 跳过空行
                continue
            cut_line = mt.tokenize(line, return_str=True)  # 使用Moses分词器分词，返回分词后的字符串
            out_f.write(cut_line.lower() + "\n")  # 将分词结果转为小写，并写入输出文件（一行一句）
    out_f.close()  # 关闭输出文件

if __name__ == "__main__":
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser()
    # 添加参数--pair_dir/-p：原始语言对文件所在目录
    parser.add_argument(
        "-p",
        "--pair_dir",
        default=None,
        type=str,
        help="The directory which contains language pair files.",
    )
    # 添加参数--dest_dir/-d：分词结果输出目录
    parser.add_argument(
        "-d",
        "--dest_dir",
        default=None,
        type=str,
        help="The destination directory to save processed train, dev and test file.",
    )
    # 添加参数--src_lang：源语言代码，默认"de"
    parser.add_argument("--src_lang", default="de", type=str, help="source language")
    # 添加参数--trg_lang：目标语言代码，默认"en"
    parser.add_argument("--trg_lang", default="en", type=str, help="target language")

    # 解析命令行参数，结果存储为args
    args = parser.parse_args()

    # 检查是否指定了pair_dir，如未指定则抛出异常
    if not args.pair_dir:
        raise ValueError("Please specify --pair_dir")

    # 若目标目录不存在，则创建之
    if not os.path.exists(args.dest_dir):
        os.makedirs(args.dest_dir)

    # 将pair_dir和dest_dir转换为Path对象，便于后续文件路径拼接
    local_data_path = Path(args.pair_dir)  # 源语言对数据所在目录
    data_dir = Path(args.dest_dir)         # 处理后数据输出目录

    # 对训练、验证和测试集进行分词处理
    for mode in ["train", "val", "test"]:
        # 分词源语言文件，输出到目标目录
        moses_cut(
            local_data_path / f"{mode}.{args.src_lang}",  # 源语言原始文件名格式：train.de/val.de/test.de
            data_dir / f"{mode}_src.cut.txt",             # 输出源语言分词文件：train_src.cut.txt等
            lang=args.src_lang,
        )
        print(f"[{mode}] 源语言文本分词完成")
        # 分词目标语言文件，输出到目标目录
        moses_cut(
            local_data_path / f"{mode}.{args.trg_lang}",  # 目标语言原始文件名格式：train.en/val.en/test.en
            data_dir / f"{mode}_trg.cut.txt",             # 输出目标语言分词文件：train_trg.cut.txt等
            lang=args.trg_lang,
        )
        print(f"[{mode}] 目标语言文本分词完成")

    # 以下注释部分为后续扩展用途，如需将分词结果移动到新建目录可取消注释和启用
    # 创建文件夹，移动读取的文本到刚创建的文件夹里
    # if not data_dir.exists():
    #     data_dir.mkdir(parents=True)
    # for fpath in local_data_path.glob("*.txt"): # 遍历所有分词后的文件,并移动到目标文件夹
    #     fpath.rename(data_dir / fpath.name)
