# LangChain 教程

> ⚠️ **声明**：这是一个初学者在学习 LangChain 过程中整理的教程，如有不对之处请海涵指正！

本文件夹包含 LangChain 的学习教程和实战案例，涵盖模型调用、提示词模板、Chain、Memory、Tools、Agents 和 RAG 等核心内容。

## 教程章节

### 1. 入门介绍 (chapter01_intro)

- **HelloWorld.ipynb**: LangChain 入门示例

### 2. 模型调用 (chapter02_Model_IO)

- **模型调用/**: OpenAI API 调用
  - 01-04-模型调用*.ipynb: 各种模型调用方式
- **提示词模板/**: Prompt 工程
  - PromptTemplate、ChatPromptTemplate 使用
  - 少量示例提示词
  - 从文件读取提示词
- **输出解析器/**: Output Parser
  - 01-输出解析器的使用.ipynb
- **调用本地大模型/**: 本地模型部署

### 3. Chain (chapter03_Chain)

- **01-基础Chain的使用.ipynb**: LLMChain、SequentialChain
- **02-基于LCEL语法的新的Chain.ipynb**: LCEL 语法

### 4. Memory (chapter04_memory)

- **01-Memory的使用.ipynb**: 基础 Memory
- **02-Memory的使用.ipynb**: 进阶 Memory

### 5. Tools (chapter05_tools)

- **01-工具的使用.ipynb**: 自定义 Tools

### 6. Agents (chapter06_agents)

- **01-传统的方式.ipynb**: 传统 Agent 实现
- **02-多工具使用.ipynb**: 多 Tool 协作
- **03-通用的方式.ipynb**: 通用 Agent
- **04-Agent中使用Memory.ipynb**: Agent + Memory

### 7. RAG (chapter07_RAG)

- **01-文档加载器的使用.ipynb**: 文档加载
- **02-文档拆分器的使用.ipynb**: 文本分块
- **03-文档嵌入模型的使用.ipynb**: Embedding
- **04-向量数据库的使用.ipynb**: Chroma、FAISS
- **05-检索器的使用.ipynb**: Retriever
- **06-综合案例.ipynb**: 完整 RAG 案例
- **asset/**: 测试数据和资源

## 核心知识点

- LangChain 基础架构
- LLM 模型调用
- Prompt 工程
- Chain 链式调用
- Memory 对话记忆
- Tools 工具扩展
- Agents 智能代理
- RAG 检索增强生成

## 环境依赖

```bash
pip install langchain langchain-openai langchain-community chromadb faiss-cpu
```

## 注意事项

- 需要 OpenAI API Key 或其他大模型 API
- 部分功能需要网络访问
- RAG 需要向量数据库支持
