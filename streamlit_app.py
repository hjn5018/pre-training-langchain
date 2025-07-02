# streamlit_app.py

import streamlit as st
from dotenv import load_dotenv
import os
from langchain_openai import OpenAI

# 환경 변수 로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 페이지 설정
st.set_page_config(
    page_title="한국 관광지 추천",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 사이드바 ---
with st.sidebar:
    st.markdown("## 설정")
    st.markdown("관광지 추천 옵션을 선택하세요.")
    
    num_places = st.selectbox("추천 받을 관광지 수", [3, 5, 7, 10], index=0)

    theme = st.selectbox(
        "여행 테마 선택",
        ["전체", "자연", "역사/문화", "음식", "액티비티", "가족 여행"],
        index=0
    )

    region = st.text_input("여행 지역 (선택사항)", placeholder="예: 서울, 제주도")

    temperature = st.slider(
        "LLM 창의성 (Temperature)", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.7, 
        step=0.1, 
        help="값이 클수록 다양하고 창의적인 응답을 생성합니다."
    )

    user_prompt = st.text_area(
        "질문 내용",
        f"한국의 대표적인 관광지 {num_places}군데를 추천해주세요.",
        height=100
    )

    recommend_btn = st.button("관광지 추천받기")

# --- 메인 화면 ---
st.title("🇰🇷 한국 관광지 추천 시스템")
st.markdown(
    """
    여행을 준비 중이신가요?  
    이 앱은 OpenAI의 LLM을 기반으로, 한국에서 꼭 가봐야 할 관광지를 추천해드립니다.
    """
)
st.markdown("---")

# 결과 처리
if recommend_btn:
    with st.spinner("추천 중입니다. 잠시만 기다려주세요..."):
        try:
            # temperature 반영된 LLM 초기화
            llm = OpenAI(temperature=temperature)

            # 사용자 옵션에 따라 프롬프트 생성
            final_prompt = f"{region + ' 지역에서' if region else ''} "
            final_prompt += f"{theme if theme != '전체' else ''} 테마로 "
            final_prompt += f"{num_places}군데의 한국 관광지를 추천해줘. "
            final_prompt += f"요청 내용: {user_prompt}"

            response = llm.invoke(final_prompt)
            st.success("추천이 완료되었습니다!")
            st.markdown("### 📝 추천 결과")
            st.text_area("관광지 리스트", response, height=250)
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")

# 푸터
st.markdown("---")
st.caption("© 2025 Korea Travel AI | Powered by LangChain & OpenAI")
