from dotenv import load_dotenv

load_dotenv()

from langchain_openai import OpenAIEmbeddings

embeddings_model = OpenAIEmbeddings()

embeddings = embeddings_model.embed_documents(
    [
        '안녕하세요!',
        '어! 오랜만이에요',
        '이름이 어떻게 되세요?',
        '날씨가 추워요',
        'Hello LLM!'
    ]
)
# print(len(embeddings))
# print(len(embeddings[0]))

print(embeddings)
