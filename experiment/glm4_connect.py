from openai import OpenAI

base_url = "http://192.168.110.131:9091/v1/"
client = OpenAI(api_key="EMPTY", base_url=base_url)

messages = [{"role": "user", "content": "你好，请你介绍一下你自己"}]

response = client.chat.completions.create(
    model="glm-4",
    messages=messages,
)

print(response.choices[0].message.content)