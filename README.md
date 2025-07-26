# 🧠 RAG-based ChatBot System

This project implements a Retrieval-Augmented Generation (RAG) based chatbot system. It supports document upload, vectorization with Qdrant, semantic retrieval, and answer generation using a remote large language model (LLM).

---

## 🗂️ Project Structure

```
chatbot_rag_backend/
├── app/
│   ├── api/                # API routes
│   │   ├── upload.py       # Upload endpoint
│   │   └── chat.py         # Chat endpoint
│   ├── services/           # Core logic
│   │   ├── embedding.py
│   │   ├── vector_store.py
│   │   ├── file_parser.py
│   │   └── rag_pipeline.py
│   ├── config.py           # Global configuration
│   └── main.py             # FastAPI entrypoint
│
├── ui/
│   └── main_ui.py          # tkinter-based desktop UI
│
├── data/uploads/           # Uploaded files
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Installation & Startup

### ✅ 1. Setup Environment

```bash
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### ✅ 2. Start FastAPI Service (Local ChatBot + Qdrant)

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

APIs:
- `/api/upload` – File upload
- `/api/chat` – Question answering

---

### ✅ 3. Start Remote GPT Model Server

```bash
cd gpt_server/
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Sample Request:

```json
POST /chatbot
{
  "context": "...",
  "question": "What is Qdrant?"
}
```

---

### ✅ 4. Start Local tkinter UI

```bash
python ui/main_ui.py
```

Provides a simple GUI for file upload and Q&A.

---

## 🧪 Example Request

```bash
curl -X POST http://localhost:8000/api/chat   -H "Content-Type: application/json"   -d '{"question": "What is vector search?"}'
```

---

## 🧠 Tech Stack

| Module         | Tech                          |
|----------------|-------------------------------|
| Vector Store   | Qdrant (via qdrant-client)    |
| Embedding      | HuggingFace Embeddings        |
| Parsing        | pdfplumber / docx / unstructured |
| Retrieval + Gen| Custom RAG pipeline           |
| Model Serving  | LLaMA / Mistral via Transformers |
| API Backend    | FastAPI                       |
| UI             | Tkinter                       |

---

## 📁 .env Sample

```env
REMOTE_LLM_ENDPOINT=http://58.xx.xx.xx:8000/chat
UPLOAD_DIR=data/uploads
```

---

## 🚧 TODO

- [ ] Multi-turn dialogue
- [ ] File preview in upload
- [ ] API Token authentication
- [ ] Streaming response support

---

## 📬 Contact

Feel free to open an issue or contribute to improve the project!