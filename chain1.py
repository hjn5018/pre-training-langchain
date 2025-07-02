from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from langchain_openai import OpenAI

llm = OpenAI()
result=llm.invoke("한국의 대표적인 관광지 3군데를 추천해주세요.")
print(result)