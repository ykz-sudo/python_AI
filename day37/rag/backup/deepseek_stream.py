# 作者: 王道 龙哥
# 2025年03月27日10时28分23秒
# xxx@qq.com
from openai import OpenAI
client = OpenAI(api_key="sk-8d043c487cf04418bbdcf659f052331e", base_url="https://api.deepseek.com")

# Round 1
messages = [{"role": "user", "content": "9.11 and 9.8, which is greater?"}]
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=messages,
    stream=True
)

reasoning_content = ""
content = ""

for chunk in response:
    if chunk.choices[0].delta.reasoning_content:
        reasoning_content += chunk.choices[0].delta.reasoning_content
    else:
        if chunk.choices[0].delta.content:
            content += chunk.choices[0].delta.content

print('-'*50)
print(reasoning_content)
print('*'*50)
print(content)
print('-'*50)
# Round 2
# messages.append({"role": "assistant", "content": content})
# messages.append({'role': 'user', 'content': "How many Rs are there in the word 'strawberry'?"})
# response = client.chat.completions.create(
#     model="deepseek-reasoner",
#     messages=messages,
#     stream=True
# )
# ...