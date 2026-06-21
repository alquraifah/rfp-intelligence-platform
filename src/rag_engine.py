from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS

load_dotenv()

INDEX_PATH = "faiss_index"

SYSTEM_PROMPT = """
You are an expert RFP analysis assistant.

Use the provided context to answer the question.
If the context contains partial but relevant information, summarize it clearly.
Do not say the information is unavailable unless the context has no relevant evidence at all.

When answering:
- Be specific.
- Use bullet points when useful.
- Mention uncertainty if the context is incomplete.
- Do not invent information outside the context.
"""


def load_vectorstore():
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    db = FAISS.load_local(
        INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return db


def get_llm():
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2
    )


def ask_rfp(question: str) -> dict:
    db = load_vectorstore()
    docs = db.similarity_search(question, k=5)

    context_parts = []
    sources = []

    for doc in docs:
        filename = doc.metadata.get("filename", "Unknown")
        page = doc.metadata.get("page", None)
        sheet = doc.metadata.get("sheet", None)

        context_parts.append(
            f"Source: {filename} | page: {page} | sheet: {sheet}\n"
            f"{doc.page_content}"
        )

        sources.append({
            "filename": filename,
            "page": page,
            "sheet": sheet,
            "preview": doc.page_content[:250]
        })

    context = "\n\n---\n\n".join(context_parts)

    user_prompt = f"""
Context:
{context}

Question:
{question}

Answer:
"""

    llm = get_llm()

    response = llm.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ])

    return {
        "answer": response.content,
        "sources": sources
    }


if __name__ == "__main__":
    question = input("Ask a question about the RFP documents: ")

    response = ask_rfp(question)

    print("\nANSWER:")
    print(response["answer"])

    print("\nSOURCES:")
    for source in response["sources"]:
        print(
            f"- {source['filename']} | "
            f"page: {source['page']} | "
            f"sheet: {source['sheet']}"
        )