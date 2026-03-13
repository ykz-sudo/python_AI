#%% md
# # 综合案例
# 
# ## 1、RAG结合大模型的小例子
# 
# 第1种情况：不使用RAG
#%%
from langchain_openai import ChatOpenAI
import os
import dotenv
dotenv.load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY1")
os.environ['OPENAI_BASE_URL'] = os.getenv("OPENAI_BASE_URL")

# 创建大模型实例
llm = ChatOpenAI(model="gpt-4o-mini")

# 调用
response = llm.invoke("北京有什么著名的建筑？")
print(response.content)
#%% md
# 第2种情况：使用RAG
#%%
# 1. 导入所有需要的包
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
import os
import dotenv

dotenv.load_dotenv()

# 2. 创建自定义提示词模板
prompt_template = """请使用以下提供的文本内容来回答问题。仅使用提供的文本信息，如果文本中没有相关信息，请回答"抱歉，提供的文本中没有这个信息"。

文本内容：
{context}

问题：{question}

回答：
"
"""

prompt = PromptTemplate.from_template(prompt_template)

# 3. 初始化模型
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY1")
os.environ['OPENAI_BASE_URL'] = os.getenv("OPENAI_BASE_URL")
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# 4. 加载文档
loader = TextLoader("./asset/load/10-test_doc.txt", encoding='utf-8')
documents = loader.load()

# 5. 分割文档
text_splitter = CharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=0,
    length_function=len
)
texts = text_splitter.split_documents(documents)

print(f"文档个数:{len(texts)}")

# 6. 创建向量存储
vectorstore = FAISS.from_documents(
    documents=texts,
    embedding=embeddings
)

# 7.获取检索器
retriever = vectorstore.as_retriever()

docs = retriever.invoke("北京有什么著名的建筑？")

# 8. 创建Runnable链
chain = prompt | llm

# 9. 提问
result = chain.invoke(input={"question":"北京有什么著名的建筑？","context":docs})
print("\n回答:", result.content)
#%% md
# ## 2、项目：智能对话助手
# 
# 1、提示词模板：ChatPromptTemplate、PromptTemplate等
# 
# 2、大语言模型的调用：ChatOpenAI() 、 OpenAI()
# 
# 3、(熟悉)输出解析器：JSONOutputParser、StrOutputParser
# 
# 4、Chain的使用：LLMChain、SequentialChain; | 、create_sql_query_chain
# 
# 5、关于模型调用前，给模型提供上下文信息：memory：ChatMessageHistory、ConversationBufferMemory
# 
# 6、工具的创建；工具的使用，给Agent
# 
# 7、Agent的使用：Agent ---> AgentExecutor   ---> LangGraph
# 
# 传统的方式：initialize_agent(llm = llm,agent=AgentType.XXX,tools=tools)
# 
# 通用的方式：create_xxx_agent(llm=llm,tools=tools,prompt=prompt)
#              AgentExecutor(agent=agent,toos=tools)
# 
# 8、数据的本地存储（使用向量数据库）：RAG
#    具体的流程：XxxLoader --> list[Document] --> XxxSplitter ---> list[Document] -->
#              OpenAIEmbeddings() ---> FAISS/Chroma  ---> Retriever
# 
# 
# ## 步骤1：定义工具
# 
#%%
import os
from langchain_community.tools.tavily_search import TavilySearchResults

# 定义 AVILY_KEY 密钥
import dotenv
dotenv.load_dotenv()
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY") 
# 查询 Tavily 搜索 API
search = TavilySearchResults(max_results=1)
# 执行查询
res = search.invoke("今天上海天气怎么样")
print(res)
#%% md
# ## 步骤2：Retriever
#%%
os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0 Safari/537.36"
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import dotenv
dotenv.load_dotenv()

# 1. 提供一个大模型
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY1")
os.environ['OPENAI_BASE_URL'] = os.getenv("OPENAI_BASE_URL")

embedding_model = OpenAIEmbeddings()

# 2.加载HTML内容为一个文档对象


loader = WebBaseLoader("https://zh.wikipedia.org/wiki/%E7%8C%AB")
docs = loader.load()
#print(docs)

# 3.分割文档
documents = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
).split_documents(docs)

# 4.向量化 得到向量数据库对象
vector = FAISS.from_documents(documents, embedding_model)

# 5.创建检索器
retriever = vector.as_retriever()

# 测试检索结果
#print(retriever.invoke("猫的特征")[0])
#%% md
# ## 步骤3：创建工具、工具集
# 
#%%
from langchain.tools.retriever import create_retriever_tool

# 创建一个工具来检索文档
retriever_tool = create_retriever_tool(
    retriever=retriever,
    name="wiki_search",
    description="搜索维基百科",
)

tools = [search, retriever_tool]
#%% md
# ## 步骤4：语言模型调用工具
#%%
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# 获取大模型
model = ChatOpenAI(model="gpt-4o-mini")

# 模型绑定工具
# model_with_tools = model.bind_tools(tools)
#
# # 根据输入自动调用工具
# response = model_with_tools.invoke([HumanMessage(content="今天上海天气怎么样")])
# print(f"ContentString: {response.content}")
# print(f"ToolCalls: {response.tool_calls}")

#%% md
# ## 步骤5：创建Agent程序(使用通用方式)
#%%
from langchain import hub
prompt = hub.pull("hwchase17/openai-functions-agent")

prompt.messages
#%%
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
# 创建Agent对象
agent = create_tool_calling_agent(model, tools, prompt)

# 创建AgentExecutor对象
agent_executor = AgentExecutor(agent=agent, tools=tools,verbose=True)
#%% md
# ## 步骤6：运行Agent
# 
#%%
print(agent_executor.invoke({"input": "猫的特征"}))
#%%
print(agent_executor.invoke({"input": "今天上海天气怎么样"}))
#%% md
# ## 步骤7：添加记忆
#%%
# 导入聊天历史记录相关模块
from langchain_community.chat_message_histories import ChatMessageHistory

from langchain_core.chat_history import BaseChatMessageHistory

from langchain_core.runnables.history import RunnableWithMessageHistory

# 用于存储不同会话的聊天历史
store = {}

# 调取指定session_id对应的memory
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    # 如果当前session_id不存在，则新建一个ChatMessageHistory实例
    if session_id not in store:
        store[session_id] = ChatMessageHistory()

    return store[session_id]

# 将agent_executor包装为支持历史记录的runnable
agent_with_chat_history = RunnableWithMessageHistory(
    runnable=agent_executor,# agent_executor，使用的agent对象
    get_session_history=get_session_history,# 获取指定session_id的memory
    input_messages_key="input",# 输入消息的key
    history_messages_key="chat_history",# 历史消息的key
)

# 调用带历史记录的agent，传入用户输入和会话ID
response = agent_with_chat_history.invoke(
    {"input": "Hi，我的名字是Cyber"},
    config={"configurable": {"session_id": "123"}},#指定会话ID
)

# 打印agent返回的响应
print(response)
#%%
response = agent_with_chat_history.invoke(
    {"input": "我的名字叫什么？"},
    config={"configurable": {"session_id": "123"}},#从存储的memory中获取
)

print(response)
#%%
response = agent_with_chat_history.invoke(
    {"input": "我的名字叫什么？"},
    config={"configurable": {"session_id": "345"}}, #因为这是345会话，所以无法获取123的 memory
)

print(response)