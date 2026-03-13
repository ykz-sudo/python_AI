# Day 37: DeepSeek R1 推理与 RAG 应用

本文件夹包含 DeepSeek R1 推理和 RAG（检索增强生成）应用的内容。

## 学习内容

- **inference/**: 推理代码
  - **model.py**: 模型加载
  - **generate.py**: 生成代码
  - **convert.py**: 模型转换
  - **kernel.py**: 内核代码
  - **configs/**: 配置文件
  - **requirements.txt**: 依赖

- **rag/**: RAG 应用
  - **deepseek-rag.ipynb**: RAG 实战
  - **deepseek_langchain.py**: LangChain RAG
  - **deepseek_langchain1.py**: LangChain 进阶
  - **davinci.txt**: 测试数据
  - **.env**: 环境变量

- **使用clip.ipynb**: CLIP 模型使用

## 核心知识点

- DeepSeek R1 推理
- RAG 检索增强生成
- LangChain 应用
- 向量数据库
- 知识库构建

## 适合人群

大语言模型学习者，需要掌握 RAG 技术

## 环境依赖

```bash
pip install langchain transformers chromadb torch
```

## 备注

需要 GPU 环境运行
