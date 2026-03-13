# Day 26: Seq2Seq 与 Attention

本文件夹包含 Seq2Seq 模型和注意力机制的详细内容。

## 学习内容

- **chapter_6/**:
  - **01_embedding_padding_pooling.ipynb**: 词向量基础
  - **02_embedding_rnn.ipynb**: RNN 基础
  - **04_embedding_lstm.ipynb**: LSTM 网络
  - **05_text_generation_lstm.ipynb**: LSTM 文本生成
  - **06_embedding_lstm_subword.ipynb**: Subword 分词
- **project/**: Seq2Seq 注意力项目
  - **seq2seq_attention_torch-2026-autodl.ipynb**: 完整项目
  - **transformer_带bleu-aliyun.ipynb**: 阿里云版本
  - **data_multi30k.py**: 数据处理
  - **wmt16 back/**: 德英翻译数据

## 核心知识点

- Seq2Seq 编码器-解码器
- Attention 注意力机制
- 序列到序列学习
- 机器翻译基础
- BLEU 评估指标

## 适合人群

NLP 学习者，需要掌握 Seq2Seq 和 Attention

## 环境依赖

```bash
pip install torch numpy jupyter
```
