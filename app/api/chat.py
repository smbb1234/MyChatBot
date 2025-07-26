from fastapi import APIRouter, Request
from ..services.embedding import get_embedding_model
from ..services.vector_store import QdrantStore
from ..services.rag_pipeline import run_rag_query
from ..config import REMOTE_LLM_ENDPOINT

router = APIRouter()

embedding = get_embedding_model()
vector_store = QdrantStore(embedding_model=embedding)
retriever = vector_store.get_retriever(k=5)

@router.post("/chat")
async def chat(request: Request):
    body = await request.json()
    question = body.get("question", "")
    if not question:
        return {"answer": "Please provide a question."}

    answer = run_rag_query(retriever, question, remote_llm_url=REMOTE_LLM_ENDPOINT)
    return {"answer": answer}
