# pdf_loader.py
import pdfplumber
from langchain_core.documents import Document

def load_pdf_as_documents(pdf_path: str):
    documents = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                doc = Document(
                    page_content=text,
                    metadata={"page": i + 1, "source": pdf_path}
                )
                documents.append(doc)
    return documents

pdf_filepath = './pdf/000660_SK_2023.pdf'
pages = load_pdf_as_documents(pdf_filepath)

print(pages[10])