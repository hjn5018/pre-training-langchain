# streamlit_app.py

import streamlit as st
from dotenv import load_dotenv
import os
from langchain_openai import OpenAI

# 환경 변수 로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# LLM 초기화
llm = OpenAI()

# Streamlit 앱 제목
st.title("관광지 추천 LLM")

# 설명 텍스트
st.write("아래 버튼을 클릭하면 한국의 대표적인 관광지 3곳을 추천받을 수 있어요.")

# 버튼 누르면 결과 출력
if st.button("관광지 추천받기"):
    question = "한국의 대표적인 관광지 3군데를 추천해주세요."
    with st.spinner("추천 중입니다..."):
        result = llm.invoke(question)
    st.success("추천 완료!")
    st.text_area("추천 결과", result, height=200)

