from fastapi import FastAPI, UploadFile, Form
from app.file_processor import process_file
from app.question_answer import ask_question

app = FastAPI()

@app.post("/process_file")
async def handle_file(file: UploadFile, agent_id: str = Form(...), user_id: str = Form(...)):
    return await process_file(file, agent_id, user_id)

@app.post("/ask")
async def handle_question(agent_id: str = Form(...), question: str = Form(...)):
    return await ask_question(agent_id, question)
