from django.core.management.base import BaseCommand  # 导入 Django 管理命令的基类
from chatbot_app.rag import build_index_from_folder  # 导入自定义的 FAISS 索引构建函数

class Command(BaseCommand):
    # 命令帮助信息，用于命令行 "python manage.py help build_faiss_index"
    help = '从 data/docs 构建 FAISS 索引（调用 rag.build_index_from_folder）'

    def handle(self, *args, **options):
        """
        实际执行命令的入口函数
        该函数会被 Django 调用以响应 "python manage.py build_faiss_index" 指令
        """
        # 调用自定义的构建函数，扫描 data/docs 文件夹并生成 FAISS 向量索引
        n = build_index_from_folder()
        
        # 输出执行结果到终端，显示构建出的文档片段数量（绿色高亮）
        self.stdout.write(self.style.SUCCESS(f'构建完成，文档片段数: {n}'))
