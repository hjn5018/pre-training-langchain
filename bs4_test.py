import bs4
from langchain_community.document_loaders import WebBaseLoader

url1 = "https://blog.langchain.dev/customers-replit/"
url2 = "https://blog.langchain.dev/langgraph-v0-2/"

loader = WebBaseLoader(
    web_paths=(url1, url2),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(class_=("article-header", "article-content"))
    ),
    requests_kwargs={
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
    }
)

docs = loader.load()
print(len(docs))

import json

with open("docs.json", "w", encoding="utf-8") as f:
    json.dump([doc.dict() for doc in docs], f, ensure_ascii=False, indent=2)
