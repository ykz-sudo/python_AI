## Transformer 翻译项目调参与优化建议

下面按模块列出本项目 **可以调参优化的地方 + 建议数值范围 / 典型取值**，可在 Notebook 的 `config` 或相关位置直接对应修改。

---

## 1. 模型结构相关

- **`d_model`（模型隐层维度）**
  - 典型值：256 / **512（常用）** / 768
  - 建议：
    - 显存紧张：256
    - 普通 12–24GB 显卡：512
    - 显存很宽裕：768 或 1024

- **`num_heads`（多头注意力头数）**
  - 要能整除 `d_model`
  - 建议组合：
    - `d_model=256` → `num_heads=4` 或 8
    - `d_model=512` → 8（推荐）或 4
    - `d_model=768` → 8 或 12

- **`num_encoder_layers` / `num_decoder_layers`（层数）**
  - 范围：2–12
  - 建议：
    - 小模型 / 快速实验：3–4
    - 标准配置：6 / 6
    - 性能优先：8–12（需要更多显存和训练时间）

- **`d_ff`（前馈层维度）**
  - 一般是 $4 \times d\_model$
  - 建议：
    - 若 `d_model=512` → `d_ff` 取 2048（经典配置）或 3072
    - 若 `d_model=256` → `d_ff` 取 1024–2048

- **`share_embedding`（是否共享词嵌入）**
  - 可选：`True` / `False`
  - 建议：
    - 语言相近（如德-英）：可以尝试 `True`，减小参数量，可能稍提升 BLEU
    - 显存紧张时也推荐 `True`

- **`max_length`（最大序列长度）**
  - 范围：64–256
  - 建议：
    - 若语料句子普遍较短：64 或 80
    - 通用：128
    - 若有较长句子：160–256（注意显存）

---

## 2. 训练与优化器相关

- **`lr`（基础学习率，若有 Noam 会被调度）**
  - 若使用 Noam：一般设置为 `1.0`，调度器内部再缩放
  - 若不用 Noam，直接固定学习率：
    - 范围：`1e-4` ~ `5e-4`（Adam）
    - 建议起点：`3e-4`

- **`warmup_steps`（Noam 预热步数）**
  - 范围：2000–16000
  - 建议：
    - 数据量较小 / 训练步数不多：2000–4000
    - 数据量大、训练时间长：8000–16000

- **Adam 参数 `beta1`, `beta2`, `eps`**
  - 典型：
    - `beta1 = 0.9`
    - `beta2 = 0.98`（Transformer 论文配置）
    - `eps = 1e-9`
  - 若梯度波动大，可以尝试：`beta2 = 0.997`

- **`weight_decay`（权重衰减）**
  - 若当前未用，可尝试加入：
    - 范围：`0` ~ `1e-2`
    - 建议：`1e-4` 或 `5e-4`

- **`label_smoothing`（标签平滑系数）**
  - 范围：`0.0` ~ `0.2`
  - 典型值：`0.1`
  - 可以尝试：`0.05`、`0.1`、`0.15` 对 BLEU 的影响

- **`dropout`（整体 Dropout 概率）**
  - 范围：0.0–0.3
  - 建议：
    - 数据较小 / 容易过拟合：0.2–0.3
    - 数据中等：0.1
    - 数据很大：0.1 或 0.0

- **`gradient_clip`（梯度裁剪阈值，若有）**
  - 范围：0.5–5.0
  - 常用：1.0 或 2.0

---

## 3. Batch & 采样策略相关

- **`tokens_per_batch`（每个 batch 的 token 数）**
  - 项目中是按 token 数组 batch，可调：
    - 范围：16k–64k（总 token 数）
    - 显存 8–12GB：24k–32k
    - 显存 24GB 以上：32k–64k

- **`max_tokens_per_sentence`（样本过滤长度阈值）**
  - 建议范围：128–256（多语料中很长句往往较少且噪声更高）
  - 若想更快训练：可以将最长句截断或丢弃在 128 或 160 以上

- **`batch_size_eval`（验证 / 测试 batch size 或 tokens）**
  - 支持更大（无反向传播），可设为训练的 1.5–2 倍

---

## 4. 正则化与训练流程

- **`early_stopping_patience`（早停轮数）**
  - 依据“验证集 loss 无提升的 epoch 数”
  - 建议：3–8
    - 小数据集：3–5
    - 大数据集：6–8

- **`checkpoint_interval`（保存模型间隔）**
  - 可以按 epoch 或按 step：
    - 按 epoch：每 1–2 个 epoch 保存一次
    - 按 step：每 1k–5k step 保存一次

- **`label_smoothing` + `dropout` 联合调整**
  - 若过拟合：
    - `dropout` 从 0.1 调到 0.2
    - `label_smoothing` 从 0.0 调到 0.1
  - 若欠拟合（train loss 很高）：
    - `dropout` 降到 0.1 或 0.05
    - `label_smoothing` 降到 0.05 或 0.0

---

## 5. 解码（推理）相关

- **`decode_strategy`（解码策略）**
  - 若当前为贪心解码，可尝试 **beam search**：
    - `beam_size`：3–8（典型：4 或 5）
    - `length_penalty`：0.6–1.0（典型：0.6 或 0.8）

- **`max_decode_len`（推理时最大生成长度）**
  - 一般为源句长度的 1.5–2.0 倍
  - 若直接用常数：
    - 范围：50–120
    - 短句任务：50–80
    - 一般翻译：80–100

---

## 6. 推荐三套整体配置示例

- **小模型（快速实验版）**
  - `d_model = 256`
  - `num_heads = 4`
  - `num_encoder_layers = 3`
  - `num_decoder_layers = 3`
  - `d_ff = 1024`
  - `dropout = 0.1`
  - `warmup_steps = 2000`
  - `tokens_per_batch ≈ 16000–24000`

- **标准模型（推荐先用这一套）**
  - `d_model = 512`
  - `num_heads = 8`
  - `num_encoder_layers = 6`
  - `num_decoder_layers = 6`
  - `d_ff = 2048`
  - `dropout = 0.1`
  - `label_smoothing = 0.1`
  - `warmup_steps = 4000`
  - `tokens_per_batch ≈ 24000–32000`
  - 解码：`beam_size = 4`，`length_penalty = 0.6`

- **大模型（显存充足 / 追求更高 BLEU）**
  - `d_model = 768`
  - `num_heads = 8 或 12`
  - `num_encoder_layers = 8–10`
  - `num_decoder_layers = 8–10`
  - `d_ff = 3072`
  - `dropout = 0.2`
  - `label_smoothing = 0.1–0.15`
  - `warmup_steps = 8000–12000`
  - `tokens_per_batch ≈ 32000–48000`


