import time
from functools import wraps
from dotenv import load_dotenv

# LangChain 관련 모듈
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# ✅ 데코레이터: 실행 시간 측정
def measure_time(label=""):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[{label}] 시작...")
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"[{label}] 완료 - 소요 시간: {end - start:.2f}초\n")
            return result
        return wrapper
    return decorator

@measure_time("1. PDF 로딩")
def load_pdf(path):
    loader = PyPDFLoader(path)
    return loader.load()

@measure_time("2. 문서 청킹")
def split_docs(documents, chunk_size=800, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_documents(documents)

@measure_time("3. 임베딩 및 벡터DB 생성")
def create_vectorstore(docs):
    embedding = OpenAIEmbeddings()
    return FAISS.from_documents(docs, embedding)

@measure_time("4. QA 체인 구성")
def build_qa_chain(vectordb):
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectordb.as_retriever()
    )

@measure_time("5. 질문 실행")
def run_query(qa_chain, query):
    return qa_chain.invoke({"query": query})


# ✅ 메인 실행
if __name__ == "__main__":
    load_dotenv()

    pdf_path = "./pdf/GPT프롬프트_기획서까지_코드검수안되어있음.pdf"
    query = "고전 LLM과 RAG의 차이점은?"

    # 파이프라인 실행
    documents = load_pdf(pdf_path)
    docs = split_docs(documents)
    vectordb = create_vectorstore(docs)
    qa_chain = build_qa_chain(vectordb)
    response = run_query(qa_chain, query)

    # 결과 출력
    print(f"[질문] {query}")
    print(f"[답변] {response}")
