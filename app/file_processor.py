import os
import fitz  # PyMuPDF
import docx2txt
from chromadb import Client
from chromadb.config import Settings
from dotenv import load_dotenv
from tempfile import NamedTemporaryFile

load_dotenv()

client = Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chroma_db"))

def extract_text(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".pdf":
        text = ""
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        return text
    elif ext == ".docx":
        return docx2txt.process(file_path)
    else:
        return ""

async def process_file(file, agent_id, user_id):
    temp = NamedTemporaryFile(delete=False)
    temp.write(await file.read())
    temp.close()
    text = extract_text(temp.name)

    collection = client.get_or_create_collection(name=agent_id)
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    metadatas = [{"user_id": user_id, "chunk_id": str(i)} for i in range(len(chunks))]
    ids = [f"{agent_id}_{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, metadatas=metadatas, ids=ids)
    return {"status": "success", "chunks": len(chunks)}
