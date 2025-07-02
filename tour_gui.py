from dotenv import load_dotenv
import os
import tkinter as tk
from langchain_openai import OpenAI

# 환경 변수 로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# LLM 초기화
llm = OpenAI()

# 질문
question = "한국의 대표적인 관광지 3군데를 추천해주세요."

# 버튼 클릭 시 실행할 함수
def get_answer():
    result = llm.invoke(question)
    output_text.delete("1.0", tk.END)  # 이전 결과 삭제
    output_text.insert(tk.END, result)  # 새로운 결과 출력

# GUI 생성
root = tk.Tk()
root.title("관광지 추천 LLM")

# 설명 라벨
label = tk.Label(root, text="아래 버튼을 클릭하면 한국의 관광지를 추천해드립니다.")
label.pack(pady=10)

# 버튼
button = tk.Button(root, text="관광지 추천받기", command=get_answer)
button.pack(pady=5)

# 결과 출력 텍스트 박스
output_text = tk.Text(root, height=10, width=50)
output_text.pack(pady=10)

# GUI 실행
root.mainloop()
