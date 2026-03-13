# Day 16: PyTorch 基础

本文件夹包含 PyTorch 深度学习框架的基础内容。

## 学习内容

- **1-张量操作与简单训练过程.ipynb**: PyTorch 入门
  - 张量创建与操作
  - 自动求导
  - 简单神经网络训练
- **chapter_2_torch/**: PyTorch 神经网络基础
  - **01-classification_model.ipynb**: 分类模型基础
  - **02_classification_model_more_control.ipynb**: 进阶分类模型
  - **03_regression.ipynb**: 回归模型
  - **04_classification_model-dnn.ipynb**: DNN 分类模型
  - **05_classification_model-dnn-bn.ipynb**: 带 BatchNorm 的 DNN
  - **06_classification_model-dnn-selu.ipynb**: SELU 激活函数
  - **07_classification_model-dnn-selu-dropout.ipynb**: Dropout 正则化
  - **08-09_regression-wide_deep.ipynb**: Wide & Deep 模型
  - **10_regression-wide_deep-multi-input.ipynb**: 多输入回归
  - **11_regression-wide_deep-multi-output.ipynb**: 多输出回归
  - **12-13_regression-hp-search.ipynb**: 超参数搜索

## 核心知识点

- PyTorch 张量操作
- 自动求导机制
- 神经网络构建：nn.Module
- 激活函数：ReLU、SELU、sigmoid、softmax
- BatchNorm 层
- Dropout 正则化
- Wide & Deep 模型
- 超参数调优

## 适合人群

深度学习初学者，需要掌握 PyTorch 基础

## 环境依赖

```bash
pip install torch numpy jupyter matplotlib
```
