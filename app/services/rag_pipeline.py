from typing import List
import requests
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

def format_docs(docs: List[Document]) -> str:
    """Concatenate multiple documents into a context string"""
    return "\n\n".join(doc.page_content for doc in docs)

def call_remote_llm_api(context: str, question: str, endpoint_url: str) -> str:
    """Call the remote LLM interface to get the answer"""
    payload = {
        "context": context,
        "question": question
    }
    try:
        response = requests.post(endpoint_url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json().get("answer", "No answer found.")
    except requests.exceptions.RequestException as e:
        return f"[ERROR] Failed to call remote LLM API: {e}"

def run_rag_query(
    retriever: BaseRetriever,
    question: str,
    remote_llm_url: str,
    context_prefix: str = "Use the following context to answer the question:"
) -> str:
    """
    Main entry:
    1. Retrieve context from vector database
    2. Concatenate context + question
    3. Call remote model to generate answer
    """
    docs = retriever.get_relevant_documents(question)
    context = format_docs(docs)
    full_context = f"{context_prefix}\n\n{context}"
    return call_remote_llm_api(full_context, question, remote_llm_url)
