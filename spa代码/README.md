# SpaCy Transformer 机器翻译项目

> ⚠️ **声明**：这是一个初学者在学习过程中整理的项目，如有不对之处请海涵指正！

本文件夹包含基于 SpaCy 的 Transformer 机器翻译项目，展示了如何使用 SpaCy 进行分词和翻译。

## 学习内容

- **transformer_带bleu_spa_subword.ipynb**: SpaCy + Transformer 机器翻译
  - Subword 分词
  - BLEU 评估
- **data_multi30k_spa.py**: 数据处理脚本
- **data_multi30k_spa.sh**: 数据处理脚本

## 核心知识点

- SpaCy 分词工具
- Transformer 机器翻译
- Subword 分词 (BPE)
- BLEU 评估指标
- 英德翻译

## 环境依赖

```bash
pip install spacy torch transformers sentencepiece sacrebleu
python -m spacy download en_core_web_sm
python -m spacy download de_core_web_sm
```

## 数据集

使用 Multi30k 数据集（英德翻译）

## 备注

这是一个学习 SpaCy 和 Transformer 结合的实验项目
