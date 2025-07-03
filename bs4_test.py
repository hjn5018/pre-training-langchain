import os
import bs4
import streamlit as st
from dotenv import load_dotenv

from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

# 환경 변수 로드
load_dotenv()
os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Streamlit 설정
st.set_page_config(page_title="LangChain 블로그 QA", layout="wide")
st.title("📘 LangChain 블로그 기반 질문 응답 서비스")
st.caption("Replit 및 LangGraph 관련 블로그에서 정보를 찾아 답변합니다.")

# 문서 로딩 및 전처리 캐싱
@st.cache_resource
def load_vectorstore():
    urls = [
        "https://blog.langchain.dev/customers-replit/",
        "https://blog.langchain.dev/langgraph-v0-2/"
    ]

    loader = WebBaseLoader(
        web_paths=urls,
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(class_=("article-header", "article-content"))
        ),
        requests_kwargs={
            "headers": {
                "User-Agent": os.environ["USER_AGENT"]
            }
        }
    )
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectorstore = FAISS.from_documents(split_docs, embeddings)

    return vectorstore

# 벡터스토어 및 QA 체인 구성
vectorstore = load_vectorstore()
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0, model="gpt-3.5-turbo")
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever(), return_source_documents=True)

# 사용자 입력
query = st.text_input("💬 질문을 입력하세요:", placeholder="예: Replit은 LangChain을 어떻게 사용했나요?", key="user_query")

if query:
    with st.spinner("🔍 답변 생성 중..."):
        result = qa_chain.invoke({"query": query})
        st.markdown("### 💡 답변")
        st.write(result["result"])

        st.markdown("---")
        st.markdown("### 📄 참조 문서")
        for doc in result["source_documents"]:
            source = doc.metadata.get("source", "")
            st.markdown(f"- [{source}]({source})")

