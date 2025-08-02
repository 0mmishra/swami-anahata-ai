from flask import Flask, request, Response
from flask_cors import CORS
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import requests
import os
from dotenv import load_dotenv
import openai
from io import BytesIO

load_dotenv()

# API Keys
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# --- Flask App ---
app = Flask(__name__)
CORS(app)

# --- ChromaDB & Embedder Setup (Preloaded) ---
embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./anahata_db")
collection = client.get_collection(name="vigyan_bhairav")

# --- TTS Synthesizer ---
def synthesize_voice(text):
    response = openai.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=text
    )
    return BytesIO(response.read())

# --- Chat Endpoint ---
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return {"error": "Empty question"}, 400

    # Query vector DB
    results = collection.query(query_texts=[question], n_results=5)
    docs = results["documents"][0]

    if not any(docs):
        fallback = "Beloved seeker, no wisdom rises now. Sit in stillness, and the answer shall come."
        audio_stream = synthesize_voice(fallback)
        return Response(audio_stream, mimetype="audio/mpeg", headers={"X-Answer-Text": fallback})

    context = "\n\n".join(docs)

    # Prompt for OpenRouter
    system_prompt = (
        "You are Swami Anahata, a serene, poetic Tantric teacher.\n"
        "Respond in exactly 3 to 4 poetic *lines*, calm and reflective.\n"
        "Begin with 'Dear one,' or 'Beloved seeker,' and end with a sacred blessing.\n"
        "Use spiritual, Yogic language. Only use the given context from Vigyan Bhairav Tantra.\n"
    )

    user_prompt = f"""Context from Vigyan Bhairav Tantra:
{context}

Question: {question}

Please answer briefly in 3 to 4 poetic lines only.

Swami Anahata:"""

    try:
        completion = requests.post("https://openrouter.ai/api/v1/chat/completions", json={
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.6,
            "max_tokens": 250
        }, headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5173/"  # adjust if deployed
        })

        completion.raise_for_status()
        result = completion.json()
        answer = result["choices"][0]["message"]["content"].strip()
        safe_text = answer.replace("\n", " ").replace("\r", " ").strip()

        # Voice synthesis
        audio_stream = synthesize_voice(answer)

        return Response(audio_stream, mimetype="audio/mpeg", headers={"X-Answer-Text": safe_text})

    except Exception as e:
        print("❌ Error:", e)
        fallback = "Dear one, the energies are quiet. Please return in stillness and ask again."
        audio_stream = synthesize_voice(fallback)
        return Response(audio_stream, mimetype="audio/mpeg", headers={"X-Answer-Text": fallback})


# --- Start Flask App ---
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)  # ✅ reloader off to prevent socket crash
