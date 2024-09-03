import os
import openai
from dotenv import load_dotenv



# 设置 API 密钥
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY  # 添加这行代码来设置 API 密钥

client = openai.OpenAI(api_key=OPENAI_API_KEY)


# 定义一个函数来调用 OpenAI API
def ask_openai(question):
    completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
    return completion.choices[0].message.content.strip()

# 示例调用
question = "當我不想工作時，可以做些什麼，同時可以放鬆和學習？"
answer = ask_openai(question)
if answer:
    print(answer)
else:
    print("Failed to get a response from OpenAI.")
