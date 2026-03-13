# 导入操作系统模块，用于文件和路径操作，比如拼接路径、检测文件夹是否存在等
import os
# 导入OpenAI的嵌入模型，用于把文本转换为向量，适配后续的向量化检索
from langchain_openai import OpenAIEmbeddings
# 导入LangChain社区的FAISS向量数据库，负责高效的向量查找与本地索引管理
from langchain_community.vectorstores import FAISS
# 导入文本分割器，将大文本切分为较小块，提高检索灵活性
from langchain_text_splitters import CharacterTextSplitter
# 导入文档数据结构，用于存储每一块文本及其元数据（如来源、序号）
from langchain_core.documents import Document
# 引入dotenv是为了兼容环境变量加载（可选）

import dotenv

# 获取项目根目录（即当前文件的上两级目录，用于定位索引等数据存放路径）
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# 设置FAISS索引文件的保存路径（如 .../faiss_index/）
INDEX_PATH = os.path.join(BASE_DIR, 'faiss_index')


def load_faiss_index():
    """
    详细介绍：

    该函数用于加载本地已有的 FAISS 向量数据库，以便实现对知识库内容的高效相似性检索。
    
    主要涉及以下接口和原理：

    1. os.path.exists(path)
        - 用于判断指定路径（INDEX_PATH）是否存在。INDEX_PATH 是 FAISS 索引的本地持久化文件夹。
        - 原理：先判断是否已成功构建索引，避免文件不存在时出错。
        - 用法：如果目录不存在，抛出 FileNotFoundError，提示用户先运行索引构建命令。

    2. OpenAIEmbeddings
        - 来自 langchain_openai 库，是一个嵌入接口，用于将文本（如问题、知识片段）编码为稠密向量。
        - 用法：实例化时可指定 embedding model（如 "text-embedding-3-small"），以确保与索引构建阶段使用相同的模型，避免向量维数不符。
        - 原理：底层会调用 OpenAI API，将输入字符串编码为高维语义向量，为后续向量检索提供基础。

    3. FAISS.load_local
        - 来自 langchain_community.vectorstores.FAISS 类。
        - 用法：`FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)`
        - 功能：从本地磁盘加载已保存的 FAISS 向量数据库，并绑定刚才生成的 embedding 实例（这样检索器才能把检索请求的 query 文本编码成同样空间的向量）。
        - 参数
            - INDEX_PATH：索引文件夹所在路径
            - embeddings：必须与构建时一致的 embedding 实例
            - allow_dangerous_deserialization：新版本 LangChain 序列化方案的兼容性参数
        - 原理：
            - FAISS 本质是 Facebook AI Research 提供的高性能向量相似性检索库，LangChain 提供了文档级的 Python 封装。
            - 本接口会读取索引文件内容，结合 embeddings 模型，恢复出向量数据库对象，进而可以快速检索近似文本。

    返回值：
        - db：恢复后的 FAISS 向量数据库对象，可以用于后续的 `.as_retriever()` 或 `.similarity_search()` 等调用。

    用法举例：
        db = load_faiss_index()
        retriever = db.as_retriever()
        docs = retriever.invoke("考研报名时间是什么时候？")
    """
    # 判断索引文件夹是否存在
    if not os.path.exists(INDEX_PATH):
        raise FileNotFoundError(
            'FAISS index not found. Please run `python manage.py build_faiss_index`'
        )
    # 初始化与索引构建阶段一致的 OpenAI 嵌入模型
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    # 利用 FAISS.load_local 接口加载本地向量数据库，绑定 embedding
    db = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    return db


def answer_with_rag(question: str, chat_history=None):
    """
    基于RAG(检索增强)方案回答用户问题，支持对话历史上下文。
    
    参数:
        question: str，用户当前问题
        chat_history: 可选，历史对话（内容格式: [{"role":"user/assistant", "content":"文本"}, ...]）
    返回:
        (answer, sources): 返回答案文本和来源标识列表（二元组）
    """
    try:
        # 加载本地知识库索引，确保已先构建
        db = load_faiss_index()
    except Exception as e:
        # 如加载失败（比如用户尚未构建索引），则返回错误提示和空来源
        return (f"知识库未构建，请联系管理员或运行构建脚本。{e}", [])
    
    # 转为检索器，设置每次检索返回得分最高的4条文本片段
    retriever = db.as_retriever(search_kwargs={'k': 4})
    
    # 延迟导入大语言模型与对话消息类型，便于加速模块导入
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
    
    # 初始化ChatOpenAI (此处使用“gpt-5-nano”，温度1代表输出更多样)
    llm = ChatOpenAI(model="gpt-5-nano", temperature=1)
    
    # 检索与当前问题最相关的知识库文档片段
    try:
        docs = retriever.invoke(question)  # 推荐调用LangChain新接口
    except AttributeError:
        # 兼容性适配（旧版本写法，invoke不可用时回退get_relevant_documents）
        docs = retriever.get_relevant_documents(question)
    
    # 拼接所有相关知识片段内容，作为上下文
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # 构建大语言模型输入的消息队列
    messages = []
    
    # 构造系统提示词，告诉模型它的身份、背景知识（知识库），要求礼貌作答
    system_prompt = f"""你是一个智能客服助手。请根据以下知识库内容回答用户问题。
如果知识库中没有相关信息，请礼貌地告知用户。

知识库内容：
{context}

请结合对话历史和知识库内容，给出准确、友好的回答。"""
    
    # 系统提示插入消息队列，成为LLM提示的第一条（SystemMessage类型）
    messages.append(SystemMessage(content=system_prompt))
    
    # 插入历史对话（仅保留最近10条历史，等价5轮完整问答；太多则截断）
    if chat_history:
        recent_history = chat_history[-10:]  # 若历史超长只要最新10条
        for msg in recent_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
    
    # 将当前用户提问包装为HumanMessage加入输入队列
    messages.append(HumanMessage(content=question))
    
    # 全部准备好后，向大语言模型发起推理调用，获得回答
    response = llm.invoke(messages)
    # 提取纯文本答案
    answer = response.content
    
    # 返回答案文本以及用于溯源的来源标识（local_faiss表示来源本地知识库）
    return (answer, ['local_faiss'])


def build_index_from_folder(folder='data/docs'):
    """
    遍历指定目录及子目录下所有txt文档，
    分割内容为小块，向量化，并建立FAISS本地索引。

    参数:
        folder: 文档目录路径。默认 'data/docs'。
    返回:
        索引包含的总文档片段数（int）。
    """
    # 动态导入glob，用于递归检索所有txt文件路径
    import glob
    # 查找目录及所有子目录下名为*.txt的文件
    files = glob.glob(os.path.join(folder, '**', '*.txt'), recursive=True)
    # texts用于存放每个文件的正文大字符串
    texts = []
    # metadatas记录每个文本串来源（源文件路径）
    metadatas = []
    # 遍历所有txt文件，将内容与文件元数据分别提取
    for f in files:
        # 打开txt文件，确保UTF-8编码兼容中文
        with open(f, 'r', encoding='utf-8') as fh:
            # 读取全文件的字符串
            txt = fh.read()
            # 把读取的文本追加到总文本列表
            texts.append(txt)
            # 文件路径作为元数据追加，后续分割需追踪原文件出处
            metadatas.append({'source': f})

    # 实例化字符级分割器，每块最大1000字符，前后块重叠200字符（防止知识断层）
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    # docs列表收集所有Document对象（即所有文本块及其元数据）
    docs = []
    # 遍历原始文本及其元数据，每条一一对应
    for t, m in zip(texts, metadatas):
        # 每条大文本分割成若干块，每块块号单独记录
        for i, chunk in enumerate(splitter.split_text(t)):
            # 创建Document对象，注入页内容，来源文件和块的编号
            docs.append(Document(page_content=chunk, metadata={**m, 'chunk': i}))

    # 初始化OpenAI嵌入模型，再次指定模型名
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    # “docs”列表输入到FAISS索引构造器，完成所有块的向量化
    db = FAISS.from_documents(docs, embeddings)
    # 如索引目录不存在则创建新的目录（递归安全）
    if not os.path.exists(INDEX_PATH):
        os.makedirs(INDEX_PATH)
    # 将构建好的FAISS索引数据保存在本地（以便下次快速加载）
    db.save_local(INDEX_PATH)
    # 返回所有分块后文档条数，外部可用来展示构建进度
    return len(docs)
