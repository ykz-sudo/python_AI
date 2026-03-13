from django.db import models  # 导入 Django 的模型模块，所有模型都要继承自 models.Model
import uuid  # 导入 uuid 模块，用于生成全局唯一的会话 ID


# 联系人模型
# 用于从文本中提取并存储联系方式，比如邮箱、电话等
class Contact(models.Model):
    # 主键，使用 BigAutoField，大整数自增主键，显式定义
    id = models.BigAutoField(primary_key=True)
    # 原始文本内容，存储提取联系方式之前的原文
    source_text = models.TextField()
    # 联系方式类型，如 'email', 'phone' 等，最大长度 32 字符
    contact_type = models.CharField(max_length=32)
    # 具体联系方式值，比如一个邮箱地址或电话号码，最大长度 128 字符
    contact_value = models.CharField(max_length=128)
    # 记录创建时间，自动设置为记录创建时的时间戳
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # 返回人类可读的字符串描述，形如 "email: example@qq.com"
        return f"{self.contact_type}: {self.contact_value}"


# 负面反馈模型
# 用于保存用户针对内容的负面反馈信息
class NegativeFeedback(models.Model):
    # 主键，使用 BigAutoField
    id = models.BigAutoField(primary_key=True)
    # 收到反馈的原始文本内容
    source_text = models.TextField()
    # 反馈原因，最大长度 256 字符，可为空或留空
    reason = models.CharField(max_length=256, null=True, blank=True)
    # 创建时间，自动填充
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # 例："Negative @ 2024-05-01 20:00:00"
        return f"Negative @ {self.created_at}"


# 聊天会话模型
# 用于管理一个用户会话（多轮对话）
class ChatSession(models.Model):
    # 主键，BigAutoField，自增大整型
    id = models.BigAutoField(primary_key=True)
    # 全局唯一的会话 ID，自动生成，不可编辑
    session_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    # 用户名／用户标识，默认值为 'anonymous'
    user = models.CharField(max_length=128, default='anonymous')
    # 会话创建时间（首次创建时自动填充）
    created_at = models.DateTimeField(auto_now_add=True)
    # 会话最近一次更新时间（每次保存对象时自动更新时间戳）
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # 形如 "Session xxxxxxxx-xxxx-... - 用户名"
        return f"Session {self.session_id} - {self.user}"

    class Meta:
        # 元数据配置，按最后更新时间降序排列（新的会话排在前面）
        ordering = ['-updated_at']


# 聊天消息模型
# 用于记录每个会话的每一条消息
class ChatMessage(models.Model):
    # 主键，BigAutoField
    id = models.BigAutoField(primary_key=True)
    # 关联会话，外键字段，CASCADE 逻辑代表会话被删除则消息一同被删
    # related_name='messages' 便于通过 session.messages 反查消息列表
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    # 消息角色字段，消息身份，user 表示用户消息，assistant 表示助手消息
    role = models.CharField(
        max_length=16,
        choices=[('user', '用户'), ('assistant', '助手')]
    )
    # 消息内容正文，TextField 支持任意长度文本
    content = models.TextField()
    # 消息创建时间（自动填充为消息创建瞬间）
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # 返回角色与消息内容前 50 字符预览
        return f"{self.role}: {self.content[:50]}"

    class Meta:
        # 元数据配置，消息按创建时间正序排列（早的在前）
        ordering = ['created_at']
