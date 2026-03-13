import re  # 导入正则表达式模块，用于匹配手机号、微信号等
import json  # 导入 JSON 解析模块，用于请求数据和 LLM 结果的解析
from django.http import JsonResponse  # 导入 JsonResponse，用于返回 JSON 格式的响应
from django.shortcuts import render  # 导入渲染模板的函数 render
from django.views.decorators.csrf import csrf_exempt  # 关闭 CSRF 校验装饰器，用于兼容前端调用
from .models import Contact, NegativeFeedback, ChatSession, ChatMessage  # 导入自定义的数据库模型
from .rag import answer_with_rag  # 导入基于 RAG 的问答实现函数
import uuid  # 用于生成随机会话UUID
import os  # 可用于获取环境变量等
from langchain_openai import ChatOpenAI  # 导入 LLM API 用于兜底抽取
from .db_tools import save_contact  # 封装好的联系方式保存函数

# 匹配中国大陆手机号的正则表达式（可包含国际区号，例如+86-13900000000）
PHONE_RE = re.compile(r"(\+?\d{2,4}[- ]?)?(1[3-9]\d{9})")
# 匹配微信号（6-20 字母/数字/下划线/短横线，非纯数字）
WECHAT_RE = re.compile(r"\b[0-9A-Za-z_-]{6,20}\b")
# 匹配 QQ 号（5-12 位数字，且首位非 0）
QQ_RE = re.compile(r"\b[1-9][0-9]{4,11}\b")
# 负面关键词列表，用于简单判定负面反馈（可根据业务优化）
NEGATIVE_KEYWORDS = ['不满意', '差', '投诉', '糟糕', '失望', '不靠谱', '差评', '无法', '垃圾']

def chat_view(request):
    """
    渲染前端的聊天页面视图
    """
    return render(request, 'chat.html')

@csrf_exempt  # 允许无 CSRF Token 的跨域请求，方便前端 Ajax 调用
def api_chat(request):
    """
    聊天主接口：接收用户消息，抽取联系方式和负面反馈，进行问答，返回结果。
    支持多轮会话，具备 LLM 和正则联动的信息抽取能力。
    """
    # 安全校验，仅允许 POST
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    # --- 解析请求体参数 ---
    data = json.loads(request.body.decode('utf-8'))
    msg = data.get('message', '')  # 用户输入的文本
    user = data.get('user', 'anonymous')  # 用户唯一标识，默认 anonymous
    session_id_str = data.get('session_id', None)  # 会话ID，用于实现多轮对话

    # --- 获取或创建会话记录 ---
    if session_id_str:
        # 如果带有 session_id 尝试用UUID还原 session对象
        try:
            session_uuid = uuid.UUID(session_id_str)
            session = ChatSession.objects.filter(session_id=session_uuid).first()
            if not session:
                # 找不到历史会话，新建一个
                session = ChatSession.objects.create(user=user)
        except (ValueError, AttributeError):
            # session_id格式不对也新建
            session = ChatSession.objects.create(user=user)
    else:
        # 首轮无 session_id，新建
        session = ChatSession.objects.create(user=user)
    
    # --- 记录用户消息 ---
    ChatMessage.objects.create(session=session, role='user', content=msg)

    # --- 优先用正则尝试提取并存储联系方式 ---
    contact_recorded = False  # 标志：是否已保存联系方式
    m = PHONE_RE.search(msg)
    if m:
        # 若匹配到手机号，优先提取第二组纯手机号
        phone = m.group(2) if m.groups() else m.group(0)
        Contact.objects.create(source_text=msg, contact_type='phone', contact_value=phone)
        contact_recorded = True

    mqq = QQ_RE.search(msg)
    if mqq:
        # 若匹配到QQ号，直接保存
        qq = mqq.group(0)
        Contact.objects.create(source_text=msg, contact_type='qq', contact_value=qq)
        contact_recorded = True

    # 微信账号需要特定关键词命中后才抽取，防止误识别
    if '微信' in msg or 'wx' in msg.lower() or 'wechat' in msg.lower():
        mwx = WECHAT_RE.search(msg)
        if mwx:
            Contact.objects.create(source_text=msg, contact_type='wechat', contact_value=mwx.group(0))
            contact_recorded = True

    # --- 如正则全未命中，则调用 LLM 兜底提取联系方式 ---
    if not contact_recorded:
        try:
            # 调用模型（可根据需要调整温度和模型名）
            llm = ChatOpenAI(model="gpt-5-nano", temperature=1)
            prompt = (
                "你是信息抽取助手。请从如下文本中抽取用户联系方式（手机、微信、QQ、邮箱或其它）。"
                "如果不存在联系方式，返回：{\"has_contact\": false}。"
                "如果存在，返回严格的JSON："
                "{\"has_contact\": true, \"type\": \"phone|wechat|qq|email|other\", \"value\": \"具体值\"}。\n"
                f"文本：{msg}"
            )
            resp = llm.invoke(prompt)
            # 对 LLM 返回结果做健壮兼容
            content = getattr(resp, "content", str(resp))
            data = json.loads(content)
            if isinstance(data, dict) and data.get("has_contact") and data.get("value"):
                ctype = (data.get("type") or "other").lower()
                cvalue = str(data.get("value"))
                # 使用封装的 save_contact 存DB（防止重复/增强兼容性）
                save_contact(source_text=msg, contact_type=ctype, contact_value=cvalue)
                contact_recorded = True
        except Exception:
            # LLM 调用失败等异常兜底不影响主流程
            pass

    # --- 负面反馈抽取 ---
    feedback_recorded = False
    # 首先遍历关键词快速命中
    for kw in NEGATIVE_KEYWORDS:
        if kw in msg:
            NegativeFeedback.objects.create(source_text=msg, reason=kw)
            feedback_recorded = True
            break

    # 如果关键词都未命中，则再用 LLM 进行语义识别
    if not feedback_recorded:
        try:
            llm = ChatOpenAI(model="gpt-5-nano", temperature=1)
            prompt = (
                "你是一个服务反馈识别助手。请判断下面文本是否表达负面反馈（不满意、投诉、批评、建议改进等）。"
                "仅返回严格的JSON：如果是负面反馈，"
                "{\"is_negative\": true, \"reason\": \"一句话原因或关键词\"};"
                "如果不是，{\"is_negative\": false}。文本：\n"
                f"{msg}"
            )
            resp = llm.invoke(prompt)
            content = getattr(resp, "content", str(resp))
            data = json.loads(content)
            if isinstance(data, dict) and data.get("is_negative"):
                NegativeFeedback.objects.create(
                    source_text=msg,
                    reason=str(data.get("reason", ""))[:256]  # 最多保留 256 字防止入库溢出
                )
                feedback_recorded = True
        except Exception:
            # LLM 抽取失败忽略
            pass

    # --- 构建多轮对话历史，支持上下文 ---
    # 获取历史消息，时间升序排列，只取最近 10 轮 (即 20 条消息；不含刚保存的这条)
    all_messages = list(ChatMessage.objects.filter(session=session).order_by('created_at'))
    history_messages = all_messages[:-1][-20:] if len(all_messages) > 1 else []
    # 转换为 RAG 需要的格式（role/content)
    chat_history = [{"role": msg.role, "content": msg.content} for msg in history_messages]
    
    # --- RAG 检索增强：生成 AI 回答，并返回相关知识点 ---
    answer, sources = answer_with_rag(msg, chat_history=chat_history)

    # --- 拼接前缀，如已记录联系方式或反馈需先表述感谢/确认 ---
    prefix_parts = []
    if contact_recorded:
        prefix_parts.append("已经将你的联系方式记录，后面会客服联系你；")
    if feedback_recorded:
        prefix_parts.append("非常感谢你的意见，我们会积极努力改进")
    final_answer = "".join(prefix_parts) + (answer or "")
    
    # --- 保存 AI 回复到消息表 ---
    ChatMessage.objects.create(session=session, role='assistant', content=final_answer)
    
    # --- 组织 API 返回结构 ---
    return JsonResponse({
        'answer': final_answer,               # 最终回复文本
        'sources': sources,                   # 检索证据/知识来源
        'session_id': str(session.session_id) # 用于前端维护多轮会话
    })

def health_check(request):
    """
    健康检查接口：用于监控服务可用性、负载均衡探活等
    """
    return JsonResponse({'status': 'ok'})

def sessions_view(request):
    """
    管理后台/调试用：展示最近多个会话及消息统计
    """
    sessions = ChatSession.objects.all().prefetch_related('messages')[:20]  # 最近20个会话（按默认排序）
    total_sessions = ChatSession.objects.count()  # 总会话数
    total_messages = ChatMessage.objects.count()  # 总消息数
    return render(request, 'sessions.html', {
        'sessions': sessions,
        'total_sessions': total_sessions,
        'total_messages': total_messages
    })
