import os
import re
import pdfplumber
import pandas as pd
from docx import Document
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def read_pdf(file_path):
    documents = []

    try:
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()

                if text:
                    documents.append({
                        "text": clean_text(text),
                        "metadata": {
                            "filename": os.path.basename(file_path),
                            "page": page_num
                        }
                    })
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")

    return documents


def read_docx(file_path):
    documents = []

    try:
        doc = Document(file_path)

        text = []

        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text.append(paragraph.text)

        if text:
            documents.append({
                "text": clean_text(" ".join(text)),
                "metadata": {
                    "filename": os.path.basename(file_path),
                    "page": None
                }
            })

    except Exception as e:
        print(f"Error reading DOCX {file_path}: {e}")

    return documents

def read_excel(file_path):
    documents = []

    try:
        excel_file = pd.ExcelFile(file_path)

        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)

            text = df.astype(str).to_string(index=False)

            if text.strip():
                documents.append({
                    "text": clean_text(text),
                    "metadata": {
                        "filename": os.path.basename(file_path),
                        "sheet": sheet_name,
                        "page": None
                    }
                })

    except Exception as e:
        print(f"Error reading Excel {file_path}: {e}")

    return documents

def load_documents(data_folder="data"):
    all_documents = []

    for root, dirs, files in os.walk(data_folder):
        for file in files:
            file_path = os.path.join(root, file)
            file_lower = file.lower()

            if file_lower.endswith(".pdf"):
                print(f"✓ Reading PDF: {file}")
                all_documents.extend(read_pdf(file_path))

            elif file_lower.endswith(".docx"):
                print(f"✓ Reading DOCX: {file}")
                all_documents.extend(read_docx(file_path))

            elif file_lower.endswith(".xlsx"):
                print(f"✓ Reading Excel: {file}")
                all_documents.extend(read_excel(file_path))

            else:
                print(f"⚠ Skipping unsupported file: {file}")

    return all_documents


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = []

    for doc in documents:
        split_texts = splitter.split_text(doc["text"])

        for chunk in split_texts:
            chunks.append({
                "text": chunk,
                "metadata": doc["metadata"]
            })

    return chunks


def build_faiss_index(chunks):
    texts = [chunk["text"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    db = FAISS.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas
    )

    db.save_local("faiss_index")

    return db


def load_vectorstore():
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    db = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    return db


if __name__ == "__main__":
    load_dotenv()

    documents = load_documents("data")
    print(f"Loaded documents: {len(documents)}")

    chunks = chunk_documents(documents)
    print(f"Created chunks: {len(chunks)}")

    build_faiss_index(chunks)

    print("FAISS index saved successfully!")