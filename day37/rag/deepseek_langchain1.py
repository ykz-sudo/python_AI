# pip install langchain_openai


from langchain_openai.chat_models.base import BaseChatOpenAI

llm = BaseChatOpenAI(
    model='deepseek-chat', 
    openai_api_key='大家改为自己的API Key',
    openai_api_base='https://api.deepseek.com',
    max_tokens=1024
)

response = llm.invoke("如何学习AI")
print(response.content)