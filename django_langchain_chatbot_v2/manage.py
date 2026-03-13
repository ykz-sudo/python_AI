#!/usr/bin/env python
# manage.py 是 Django 项目的命令行工具脚本，常用于启动开发服务器、迁移数据库等操作

import os  # 用于与操作系统交互，如环境变量设置
import sys  # 提供对 Python 解释器相关功能的访问，如命令行参数

if __name__ == '__main__':
    # 设置 Django 项目的默认配置模块（settings）
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot_project.settings')
    try:
        # 从 Django 导入执行命令行指令的函数
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # 如果导入失败，重新抛出异常
        raise
    # 执行 Django 命令行工具，并传递所有的命令行参数
    execute_from_command_line(sys.argv)
