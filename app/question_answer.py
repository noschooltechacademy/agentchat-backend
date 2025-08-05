import openai
from chromadb import Client
from chromadb.config import Settings
from dotenv import load_dotenv
import os

load_dotenv()

client = Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chroma_db"))
openai.api_key = os.getenv("OPENAI_API_KEY")

async def ask_question(agent_id, question):
    collection = client.get_or_create_collection(name=agent_id)
    results = collection.query(query_texts=[question], n_results=3)
    context = " ".join(doc for doc in results["documents"][0])
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Answer using only the user's uploaded documents."},
            {"role": "user", "content": context + "\n\nQuestion: " + question}
        ]
    )
    return {"answer": response.choices[0].message.content}
