from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key =OPENAI_API_KEY) 

response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    response_format={"type": "json_object"},
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant designed to output JSON.",
        },
        {
            "role": "user",
            "content": "유머 하나 얘기해줘. "
            "난이도는 [상, 중, 하] 중 하나로 표기해 주세요.",
        },
    ],
    temperature=0.0,
    max_tokens=300,
)

for x in response.choices:
    print(x.message.content)
    print()
