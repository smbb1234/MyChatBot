import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from ..services.embedding import get_embedding_model
from ..services.vector_store import QdrantStore
from ..services.file_parser import parse_file
from ..config import UPLOAD_DIR

router = APIRouter()

embedding = get_embedding_model()
vector_store = QdrantStore(embedding_model=embedding)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith((".pdf", ".txt", ".docx")):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    try:
        docs = parse_file(file_path)
        vector_store.add_documents(docs)
        return {"message": f"File '{file.filename}' uploaded and processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")
