# pip install langchain_openai


from langchain_openai.chat_models.base import BaseChatOpenAI

llm = BaseChatOpenAI(
    model='deepseek-chat', 
    openai_api_key='sk-8d043c487cf04418bbdcf659f052331e',
    openai_api_base='https://api.deepseek.com',
    max_tokens=1024
)

response = llm.invoke("如果要从事多模态的研究，那么最应该读的论文，去代码复现的论文有哪些呢")
print(response.content)