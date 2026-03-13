# Day 21: 卷积神经网络 CNN

本文件夹包含卷积神经网络（CNN）的详细内容，包括 VGG、ResNet、InceptionNet 等经典模型。

## 学习内容

- **chapter4/**:
  - **01-classification_model_cnn.ipynb**: CNN 基础分类
  - **02-classification_model_cnn_normalize.ipynb**: 归一化 CNN
  - **03_classification_model_cnn_normalize_selu.ipynb**: SELU CNN
  - **04_classification_model_separable_cnn.ipynb**: 可分离卷积
  - **05_10_monkeys_model.ipynb**: 10 种猴子分类
  - **06_10_monkeys_model_2_resnet50_finetune.ipynb**: ResNet50 微调
  - **07_cifar10_model.ipynb**: CIFAR10 图像分类

- **chapter_4_torch_old/**: 经典 CNN 模型
  - **01-classification_model-cnn.ipynb**: CNN 基础
  - **02_classification_model-cnn-selu.ipynb**: SELU CNN
  - **03_classification_model-separable_cnn.ipynb**: 可分离卷积
  - **04_10_monkeys_model_1.ipynb**: 猴子分类基础
  - **04_10_monkeys_model_2.ipynb**: 猴子分类进阶
  - **05_10_monkeys_model_2_resnet50_finetune_1.ipynb**: ResNet50 微调
  - **06_cifar10_model_1.ipynb**: CIFAR10 基础
  - **06_cifar10_model_2.ipynb**: CIFAR10 进阶

- **chapter_6_new/**: 新模型
  - **new_vgg.ipynb**: VGG 网络
  - **new_resnet.ipynb**: ResNet 网络
  - **new_inception_net.ipynb**: InceptionNet
  - **new_vgg_fine_tuning.ipynb**: VGG 微调

## 核心知识点

- 卷积层、池化层
- 特征图可视化
- VGG 网络结构
- ResNet 残差连接
- InceptionNet 多尺度
- 可分离卷积
- 迁移学习与微调

## 适合人群

深度学习学习者，需要掌握 CNN 技术

## 环境依赖

```bash
pip install torch torchvision numpy jupyter matplotlib
```
