from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

import pandas as pd

# 데이터 로드
data = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", None],
    "Age": [25, 30, None, 28],
    "Score": [85, 90, 95, None],
    "gender": ["F", "M", "M", "F"]
})

# print(data)

# data['Name'] = data['Name'].fillna("Unknown")
# data['Age'] = data['Age'].fillna(data['Age'].mean())
# data['Score'] = data['Score'].fillna(data['Score'].mean())

# print("결측치 처리 후 데이터:")
# print(data)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, max_tokens=256)
memory = ConversationBufferMemory()

# 프롬프트 템플릿
prompt = PromptTemplate(
    template="데이터를 분석하고 인사이트를 도출하세요: {stats}\n이전 작업 내용: {history}"
)

# LangChain 체인 생성
chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

stats = data.describe()

# print("\n기술 통계:")
# print(stats)

summary = chain.run(stats=stats.to_string())
print("\nLangChain 기술 통계 요약:")
print(summary)

import matplotlib.pyplot as plt

# 히스토그램: Age
data['Age'].plot(kind='hist', title='Age Distribution', bins=5)
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()

visual_summary = chain.run(stats="Age의 분포를 보여주는 히스토그램입니다. X축은 나이, Y축은 빈도를 나타냅니다.")
print("\nLangChain 시각화 설명:")
print(visual_summary)