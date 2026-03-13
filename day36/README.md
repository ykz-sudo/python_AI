# Day 36: ChatGLM4 + LoRA 微调实战

本文件夹包含 ChatGLM4 和 LoRA 微调的实战内容。

## 学习内容

- **DeepSeekV3/inference/**: DeepSeek 推理代码
  - **model.py**: 模型加载
  - **generate.py**: 生成代码
  - **convert.py**: 模型转换
  - **kernel.py**: 内核代码
  - **configs/**: 配置文件
- **chat_robot_glm4_lora.py**: ChatGLM4 + LoRA
- **chat-robot-glm4-9b.py**: ChatGLM4-9B 机器人
- **数据预处理.py**: 数据预处理
- **eval.py / eval2.py**: 评估脚本
- **chatbot_html-master/**: Web 聊天机器人
  - **index.html**: 前端页面
  - **chat.js**: 前端逻辑

## 核心知识点

- ChatGLM4 模型
- LoRA 微调实战
- Web 聊天机器人开发
- 模型评估

## 适合人群

大语言模型学习者，需要掌握 LLM 应用开发

## 环境依赖

```bash
pip install transformers peft torch accelerate flask
```

## 备注

需要 GPU 环境运行
