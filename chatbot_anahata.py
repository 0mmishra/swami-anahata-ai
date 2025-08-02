import chromadb
from chromadb.config import Settings
import requests
import os
from dotenv import load_dotenv

# === 1. Load API key from .env ===
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# === 2. Connect to local ChromaDB ===
chroma_client = chromadb.Client(Settings(
    persist_directory="vector_db",
    anonymized_telemetry=False
))
collection = chroma_client.get_or_create_collection(name="vigyan_bhairav")

# === 3. Ask the user a question ===
question = input("🧘🏽 Ask Swami Anahata a question:\n> ")

# === 4. Query ChromaDB ===
results = collection.query(query_texts=[question], n_results=3)
chunks = results["documents"][0]
context = "\n---\n".join(chunks)

# === 5. Compose messages ===
messages = [
    {
        "role": "system",
        "content": (
            "You are Swami Anahata, a modern Tantric mystic and spiritual guide. "
            "You speak gently, with clarity and depth, always pointing the seeker inward. "
            "Use verses from the Vigyan Bhairav Tantra below to answer their question mindfully."
        )
    },
    {
        "role": "user",
        "content": f"""
Sacred Teachings from Vigyan Bhairav Tantra:
{context}

My Question:
{question}
"""
    }
]

# === 6. Call OpenRouter API ===
response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "messages": messages,
        "max_tokens": 400,
        "temperature": 0.7
    }
)

# === 7. Handle response ===
if response.status_code == 200:
    reply = response.json()["choices"][0]["message"]["content"]
    print("\n🕉️ Swami Anahata says:\n")
    print(reply.strip())
else:
    print("❌ Error:", response.status_code, response.text)

def query_anahata(question):
    from chromadb.config import Settings
    import chromadb

    chroma_client = chromadb.Client(Settings(
        persist_directory="vector_db",
        anonymized_telemetry=False
    ))
    collection = chroma_client.get_or_create_collection(name="vigyan_bhairav")

    results = collection.query(query_texts=[question], n_results=3)
    chunks = results["documents"][0]
    context = "\n---\n".join(chunks)
    return context
