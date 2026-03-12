# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI
api_key = ''
client = OpenAI(api_key=api_key, base_url="https://api.scnet.cn/api/llm/v1")

response = client.chat.completions.create(
    model="Qwen3-30B-A3B",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)