# Python-AI 学习路线

本仓库包含从 Python 基础到深度学习、大语言模型应用的完整学习路径。通过每天一个主题的方式，循序渐进地掌握 Python 编程和人工智能核心技术。

## 学习路径概览

| 阶段 | 内容 | 文件夹 |
|------|------|--------|
| 基础入门 | Python 基础语法、数据结构、函数式编程 | day1-day10 |
| 数据处理 | Pandas、NumPy、机器学习基础 | day11-day15 |
| PyTorch 深度学习 | 神经网络构建、卷积神经网络 | day16-day21 |
| 经典模型 | VGG、ResNet、InceptionNet | day22-day23 |
| NLP 入门 | RNN、LSTM、文本处理 | day24-day27 |
| Transformer | 机器翻译、BLEU评估 | day29-day31 |
| 大语言模型 | LLM推理、PEFT微调、RAG应用 | day33-day38 |

## 每日学习内容

### 第一阶段：Python 基础 (day1-day10)

- **day1**: Python 入门 - 第一个程序
- **day2**: 变量与基本数据类型
- **day3**: 数据结构 - 列表、元组、字典、集合
- **day4**: 函数基础 - 函数定义、参数、递归
- **day5**: 面向对象编程 - 类与对象、封装、继承
- **day6**: 面向对象进阶 - 多态、单例模式、异常处理
- **day7**: 文件操作与正则表达式
- **day8**: 算法基础 - 二叉树、快速排序
- **day9**: NumPy 与 Matplotlib 数据可视化
- **day10**: NumPy 进阶与数据文件处理

### 第二阶段：数据处理与机器学习 (day11-day15)

- **day11**: Pandas 数据分析基础
- **day12**: Scikit-learn 数据预处理与特征工程
- **day13**: KNN 算法与实战
- **day14**: 朴素贝叶斯、线性回归
- **day15**: 逻辑回归、聚类算法

### 第三阶段：PyTorch 深度学习 (day16-day21)

- **day16**: PyTorch 基础 - 张量操作、简单训练流程
- **day17**: Dataset 与 DataLoader
- **day18**: 回归与分类模型
- **day19**: 深度神经网络 - Dropout、BN、SeLU
- **day20**: 自定义层与损失函数
- **day21**: 卷积神经网络 CNN - VGG、ResNet、InceptionNet

### 第四阶段：经典深度学习模型 (day22-day23)

- **day22**: VGG 模型理论与实践
- **day23**: ResNet、InceptionNet 实战

### 第五阶段：自然语言处理 (day24-day27)

- **day24**: 词向量 Embedding 与 RNN
- **day25**: LSTM 文本生成
- **day26**: Seq2Seq 与 Attention 机制
- **day27**: 注意力机制进阶与 BLEU 评估

### 第六阶段：Transformer 与机器翻译 (day29-day31)

- **day29**: Transformer 架构详解
- **day30**: Transformer 训练与 BLEU 评估
- **day31**: 机器翻译项目实战

### 第七阶段：大语言模型 (day33-day38)

- **day33**: ChatGLM 模型结构与 PEFT 微调
- **day34**: (未使用)
- **day35**: DeepSeek V3 模型部署
- **day36**: ChatGLM4 + LoRA 微调实战
- **day37**: DeepSeek R1 推理与 RAG 应用
- **day38**: Dify 平台与 RAG 系统搭建

## 项目结构

```
Python-AI/
├── day1-day10/       # Python 基础
├── day11-day15/      # 数据处理与机器学习
├── day16-day21/      # PyTorch 深度学习
├── day22-day23/      # 经典模型
├── day24-day27/      # NLP 入门
├── day29-day31/      # Transformer
├── day33-day38/      # 大语言模型
```

## 环境要求

- Python 3.8+
- PyTorch 2.0+
- NumPy, Pandas, Scikit-learn
- transformers, peft, langchain
- deepseek-v3 相关依赖

## 使用方法

1. 克隆本仓库
2. 安装依赖: `pip install -r requirements.txt`
3. 按照每日顺序学习，或根据兴趣选择特定主题

## 注意事项

- 部分 notebook 包含阿里云/AutodL 训练结果
- 大语言模型相关代码需要 GPU 环境
- 建议使用 Jupyter Notebook 或 JupyterLab 运行 .ipynb 文件

## 许可证

本项目仅供学习使用。
