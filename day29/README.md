# Transformer 机器翻译项目

## 项目概述

本项目是一个基于 **Transformer 架构**的**德语到英语机器翻译系统**，使用 WMT16 数据集进行训练。项目完整实现了 Transformer 模型的核心组件，包括编码器（Encoder）、解码器（Decoder）、多头自注意力机制、交叉注意力机制等，并提供了完整的训练、评估、推理和可视化功能。

## 项目结构

```
day29/
├── transformer_带bleu-aliyun.ipynb  # 主项目文件（完整的Transformer实现）
├── data_multi30k.py                 # 数据预处理脚本（Moses分词）
├── data_multi30k.sh                 # 数据预处理Shell脚本（BPE编码）
├── wmt16/                           # WMT16数据集目录
│   ├── train.de, train.en          # 原始训练数据
│   ├── val.de, val.en              # 验证数据
│   ├── test.de, test.en            # 测试数据
│   ├── train_src.bpe, train_trg.bpe  # BPE编码后的训练数据
│   ├── bpe.20000                   # BPE编码规则文件
│   └── vocab                       # 词表文件
├── wmt16_cut/                       # Moses分词后的中间数据
├── checkpoints/                     # 模型检查点保存目录
├── runs/                           # TensorBoard日志目录
└── README.md                        # 本文件
```

## 核心功能

### 1. 数据处理模块

#### 1.1 数据预处理流程

项目采用**两阶段分词策略**：

1. **Moses分词** (`data_multi30k.py`)
   - 使用 `sacremoses` 库对德语和英语进行分词
   - 处理特殊字符、缩写、连字符等
   - 将文本转为小写

2. **BPE编码** (`data_multi30k.sh`)
   - 使用 `subword-nmt` 工具学习联合BPE编码
   - 合并源语言和目标语言数据，学习共享的BPE规则
   - BPE操作次数：20000（生成约20000个子词单元）
   - 对训练集、验证集、测试集统一应用BPE编码

#### 1.2 数据集类 (`LangPairDataset`)

- **功能**：加载BPE编码后的双语平行语料
- **特性**：
  - 自动过滤超长句子（默认最大长度512）
  - 缓存机制：处理后的数据保存为`.npy`格式，避免重复处理
  - 支持训练/验证/测试三种模式

#### 1.3 词表构建

- **特殊Token**：
  - `[PAD]`: 填充token（索引0）
  - `[BOS]`: 句子起始符（索引1）
  - `[UNK]`: 未知词（索引2）
  - `[EOS]`: 句子结束符（索引3）

- **词表规模**：约18111个词（包含特殊token和BPE子词）

### 2. Tokenizer（分词器）

实现了完整的编码/解码功能：

- **`encode()`方法**：
  - 将文本转换为索引序列
  - 支持添加BOS/EOS标记
  - 自动padding到统一长度
  - 可返回padding mask

- **`decode()`方法**：
  - 将索引序列还原为文本
  - 支持移除BOS/EOS/PAD标记
  - 支持返回单词列表或句子字符串

### 3. 批量采样器 (`TransformerBatchSampler`)

**核心创新**：按token数量而非样本数量组batch

- **传统方法**：按样本数分batch，导致：
  - 长句多时显存爆炸
  - 短句多时显存利用率低
  - 训练不均衡

- **本项目方法**：按token总数分batch
  - 每个batch包含约28000个源token和28000个目标token
  - 显存占用更稳定
  - 训练效率更高

**实现细节**：
- `SampleInfo`：记录样本索引和长度信息
- `TokenBatchCreator`：动态按token数打包样本
- `TransformerBatchSampler`：实现PyTorch的`BatchSampler`接口

### 4. Transformer模型架构

#### 4.1 嵌入层 (`TransformerEmbedding`)

- **词嵌入**：将token索引映射为向量
- **位置编码**：使用固定的正弦/余弦位置编码
  - 位置编码权重设置为不可训练（`requires_grad=False`）
- **Dropout**：防止过拟合
- **层归一化**：稳定训练

#### 4.2 注意力机制 (`MultiHeadAttention`)

**多头自注意力**：
- 将输入分为多个头，并行计算注意力
- 每个头关注不同的表示子空间
- 最后拼接所有头的输出

**交叉注意力**（Decoder专用）：
- Query来自Decoder
- Key和Value来自Encoder输出
- 实现源语言和目标语言的对齐

**注意力Mask机制**：
- **Padding Mask**：mask掉padding位置，避免模型关注无效token
- **Look-ahead Mask**：Decoder自回归时防止"偷看"未来信息（下三角mask）

#### 4.3 Transformer Block

每个Block包含三个子层：

1. **自注意力子层**（Encoder和Decoder都有）
   - 多头自注意力
   - Dropout + 残差连接 + 层归一化

2. **交叉注意力子层**（仅Decoder）
   - 多头交叉注意力
   - Dropout + 残差连接 + 层归一化

3. **前馈神经网络（FFN）**
   - 两个线性层 + ReLU激活
   - Dropout + 残差连接 + 层归一化

#### 4.4 Encoder（编码器）

- **结构**：堆叠多个Transformer Block
- **功能**：将源语言序列编码为上下文表示
- **输出**：
  - `last_hidden_states`：最后一层的隐藏状态
  - `attn_scores`：每层的自注意力分数（用于可视化）

#### 4.5 Decoder（解码器）

- **结构**：堆叠多个Transformer Block（包含交叉注意力）
- **功能**：基于Encoder输出和已生成的目标序列，预测下一个token
- **输出**：
  - `last_hidden_states`：最后一层的隐藏状态
  - `self_attn_scores`：自注意力分数
  - `cross_attn_scores`：交叉注意力分数

#### 4.6 完整模型 (`TransformerModel`)

**特性**：
- 支持共享/非共享词嵌入（`share_embedding`参数）
  - 共享：源语言和目标语言使用同一组embedding参数
  - 优点：减少参数、提升泛化（适用于相近语言）
- 权重初始化：使用Xavier均匀分布初始化
- 输出层：将Decoder隐藏状态映射到词表空间

### 5. 训练模块

#### 5.1 损失函数

- **交叉熵损失**：标准的多分类损失
- **标签平滑**：缓解过拟合，提升泛化能力
- **Padding Mask**：计算loss时忽略padding位置

#### 5.2 优化器和学习率调度

- **优化器**：Adam优化器
  - `beta1=0.9, beta2=0.98`
  - `eps=1e-9`

- **学习率调度**：Noam学习率调度策略
  ```
  lr = d_model^(-0.5) * min(step^(-0.5), step * warmup_steps^(-1.5))
  ```
  - Warmup阶段：学习率线性增长
  - 后续阶段：按 `1/sqrt(step)` 衰减
  - 默认warmup步数：4000

#### 5.3 训练流程

1. **数据加载**：使用自定义BatchSampler按token数分batch
2. **前向传播**：Encoder编码源序列，Decoder生成目标序列
3. **损失计算**：计算预测与真实标签的交叉熵损失
4. **反向传播**：计算梯度并更新参数
5. **验证评估**：定期在验证集上评估模型性能
6. **模型保存**：保存最佳模型检查点
7. **早停机制**：验证损失不再下降时提前停止训练

#### 5.4 训练配置示例

```python
config = {
    "d_model": 512,              # 隐藏层维度
    "num_heads": 8,              # 注意力头数
    "num_encoder_layers": 6,     # Encoder层数
    "num_decoder_layers": 6,     # Decoder层数
    "d_ff": 2048,                # FFN隐藏层维度
    "dropout": 0.1,              # Dropout率
    "max_length": 128,           # 最大序列长度
    "vocab_size": 18111,         # 词表大小
    "share_embedding": False,    # 是否共享词嵌入
    "pad_idx": 0,                # Padding索引
    "bos_idx": 1,                # BOS索引
    "eos_idx": 3,                # EOS索引
}
```

### 6. 评估模块

#### 6.1 损失评估

- 在验证集/测试集上计算平均损失
- 支持padding mask，只计算有效token的损失

#### 6.2 BLEU评估

- 使用NLTK的BLEU评分函数
- 计算每个样本的BLEU分数
- 输出平均BLEU分数作为翻译质量指标

### 7. 推理和可视化模块

#### 7.1 Translator类

实现了完整的翻译推理功能：

- **预处理**：
  1. Moses分词（德语）
  2. BPE编码
  3. Tokenizer编码为索引序列

- **推理**：
  1. Encoder编码源序列
  2. Decoder自回归生成目标序列
  3. 贪心解码（每次选择概率最大的token）

- **后处理**：
  1. 去除BPE粘连符号（`@@`）
  2. Moses去分词（英语）
  3. 返回可读的翻译结果

#### 7.2 注意力可视化

- **自注意力热力图**：展示Decoder内部token之间的注意力分布
- **交叉注意力热力图**：展示Decoder对Encoder输出的注意力分布
- **多头可视化**：可选择特定注意力头进行可视化
- **多层可视化**：可选择特定Transformer层进行可视化

**用途**：
- 分析模型关注的重点
- 理解翻译对齐机制
- 调试模型行为
- 发现翻译错误原因

## 技术特点

### 1. 完整的Transformer实现

- 严格按照原始论文实现所有核心组件
- 支持多头注意力、残差连接、层归一化等关键机制
- 实现了完整的Encoder-Decoder架构

### 2. 高效的数据处理

- BPE子词编码：解决OOV问题，减少词表大小
- 缓存机制：避免重复处理数据
- 按token数分batch：提高训练效率

### 3. 完善的训练流程

- Noam学习率调度：适合Transformer的训练策略
- 标签平滑：提升模型泛化能力
- 早停机制：防止过拟合
- TensorBoard日志：可视化训练过程

### 4. 丰富的评估和可视化

- BLEU评分：量化翻译质量
- 注意力可视化：理解模型行为
- 单样本分析：支持详细案例分析

## 使用说明

### 环境要求

```bash
torch >= 2.0
numpy
pandas
matplotlib
tqdm
sacremoses          # Moses分词工具
subword-nmt         # BPE编码工具
fastBPE              # 快速BPE应用
nltk                 # BLEU评估
tensorboard          # 训练可视化
```

### 数据准备

1. **下载WMT16数据集**，放置在`wmt16/`目录下
2. **运行预处理脚本**：
   ```bash
   sh data_multi30k.sh wmt16 wmt16_cut de en
   ```
   这将：
   - 对原始数据进行Moses分词
   - 学习BPE编码规则
   - 对训练/验证/测试集应用BPE编码

### 训练模型

1. **打开Jupyter Notebook**：`transformer_带bleu-aliyun.ipynb`
2. **配置超参数**：修改`config`字典
3. **运行训练代码**：执行训练cell
4. **监控训练**：使用TensorBoard查看训练日志
   ```bash
   tensorboard --logdir runs/
   ```

### 评估模型

1. **加载模型检查点**：从`checkpoints/`目录加载最佳模型
2. **运行评估代码**：在测试集上计算损失和BLEU分数
3. **分析结果**：查看翻译样例和注意力可视化

### 翻译推理

```python
# 初始化Translator
translator = Translator(model, src_tokenizer, trg_tokenizer)

# 翻译单个句子
sentence = "Ein Mann liest ein Buch."
translation = translator([sentence])

# 可视化注意力
translator([sentence], heads_list=[0, 1, 2], layer_idx=-1)
```

## 项目亮点

1. **从零实现**：不依赖预训练模型，完整实现Transformer架构
2. **工程化设计**：代码结构清晰，注释详细，易于理解和扩展
3. **性能优化**：按token数分batch、缓存机制等提升训练效率
4. **可视化分析**：注意力热力图帮助理解模型工作原理
5. **完整流程**：从数据预处理到模型训练、评估、推理的完整实现

## 文件说明

- **`transformer_带bleu-aliyun.ipynb`**：主项目文件，包含所有代码实现
- **`data_multi30k.py`**：数据预处理Python脚本（Moses分词）
- **`data_multi30k.sh`**：数据预处理Shell脚本（BPE编码流程）
- **`生成器.ipynb`**：Python生成器示例代码
- **`于孔泽.ipynb`**：其他相关代码

## 注意事项

1. **显存要求**：训练时建议使用GPU，batch_size根据显存大小调整
2. **数据路径**：确保数据文件路径正确
3. **依赖安装**：某些工具（如`subword-nmt`）可能需要单独安装
4. **BPE一致性**：训练和推理必须使用相同的BPE编码规则

## 参考资料

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) - Transformer原始论文
- [WMT16数据集](https://www.statmt.org/wmt16/multimodal-task.html#task1)
- [BPE算法](https://github.com/rsennrich/subword-nmt)

## 作者

本项目为Transformer机器翻译的完整实现，适合学习和研究使用。

---

**最后更新**：2025年1月

