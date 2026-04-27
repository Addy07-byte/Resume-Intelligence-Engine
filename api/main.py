from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chromadb
import tempfile
import os
from dotenv import load_dotenv

from core.parser import parse_resume
from core.chunker import chunk_text
from core.embedder import embed_chunks, get_embedding_model
from core.retriever import get_collection, store_embeddings, retrieve_relevant_chunks
from core.jd_processor import process_job_description
from core.generator import generate_resume

load_dotenv()

app = FastAPI(title="Resume Intelligence Engine v2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeResponse(BaseModel):
    status: str
    tailored_resume: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    files: list[UploadFile] = File(...),
    job_description: str = Form(...)
):
    try:
        client = chromadb.Client()
        collection = get_collection(client)
        model = get_embedding_model()
        contact_info = ""

        for i, file in enumerate(files):
            suffix = os.path.splitext(file.filename)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(await file.read())
                tmp_path = tmp.name

            text = parse_resume(tmp_path)
            if i == 0:
                contact_info = text

            chunks = chunk_text(text)
            embeddings, metadatas = embed_chunks(chunks, source_filename=file.filename)
            store_embeddings(collection, chunks, embeddings, metadatas)
            os.unlink(tmp_path)

        clean_jd = process_job_description(job_description)
        query_vector = model.embed_query(clean_jd)
        retrieved_chunks = retrieve_relevant_chunks(collection, query_vector, k=5)
        result = generate_resume(retrieved_chunks, clean_jd, contact_info=contact_info)

        return AnalyzeResponse(status="success", tailored_resume=result)
    except Exception as e:
        import traceback
        print(f"ERROR in /analyze: {str(e)}")
        print(traceback.format_exc())
        raise