# from dotenv import load_dotenv
# import os
# from openai import OpenAI

# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key =OPENAI_API_KEY) 

# response = client.chat.completions.create(
#     model="gpt-3.5-turbo-1106",
#     response_format={"type": "json_object"},
#     messages=[
#         {
#             "role": "system",
#             "content": "You are a helpful assistant designed to output JSON.",
#         },
#         {
#             "role": "user",
#             "content": "유머 하나 얘기해줘. "
#             "난이도는 [상, 중, 하] 중 하나로 표기해 주세요.",
#         },
#     ],
#     temperature=0.0,
#     max_tokens=300,
# )

# for x in response.choices:
#     # print(x.message)
#     print(type(x.message.content)) # <class 'str'>
#     print(x.message.content)
#     print()
# ==========================================================================================
# ==========================================================================================

# from dotenv import load_dotenv
# import os
# from openai import OpenAI

# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key =OPENAI_API_KEY) 

# def ask(question, message_history=[], model="gpt-3.5-turbo",reset=False):
#     if reset:
#         message_history = []  # 초기화

#     if len(message_history) == 0:
#         # 최초 질문
#         message_history.append(
#             {
#                 "role": "system",
#                 "content": "You are a helpful assistant. You must answer in Korean.",
#             }
#         )

#     # 사용자 질문 추가
#     message_history.append(
#         {
#             "role": "user",
#             "content": question,
#         },
#     )

#     # GPT에 질문을 전달하여 답변을 생성
#     completion = client.chat.completions.create(
#         model=model,
#         messages=message_history
#     )

#     # 사용자 질문에 대한 답변을 추가
#     message_history.append(
#         {"role": "assistant", "content": completion.choices[0].message.content}
#     )

#     return message_history

# message_history = ask("비숑은 어느나라 품종인가요?")
# print(type(message_history))
# print(message_history)
# ==========================================================================================
# ==========================================================================================

from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key =OPENAI_API_KEY) 

def question(txt1,txt2):

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
              "content": txt1 + txt2
          },
      ],
      temperature=0.5,
      max_tokens=300,
      n=5,
  )
  return response

txt1='박스플랏을 를 주제로 4지선다형 객관식 문제를 만들어주세요. answer는 1~4로 알려주세요.'
txt2='난이도는 [상, 중, 하] 중 하나로 표기해 주세요.'
result=question(txt1,txt2)

# for res in result.choices:
#     print(res.message.content)

import json
json_result = [json.loads(res.message.content) for res in result.choices]
# print(json_result)

import pandas as pd
df = pd.DataFrame(json_result)
# print(df)

df.to_csv("stats_quiz.csv", index=False)