# server.py
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import requests
import chromadb
from io import BytesIO
from dotenv import load_dotenv
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
ELEVEN_VOICE_ID = os.getenv("ELEVEN_VOICE_ID")

app = Flask(__name__)
CORS(app)  # wide-open for local dev; tighten in production

# Chroma setup (you already had this)
embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./anahata_db")
collection = client.get_collection(name="vigyan_bhairav")

# Simple in-memory audio cache (BytesIO)
audio_cache = {}

def synthesize_voice(text, cache_key):
    """
    Call ElevenLabs TTS and store MP3 bytes in audio_cache[cache_key] as BytesIO.
    """
    if not ELEVEN_API_KEY or not ELEVEN_VOICE_ID:
        print("❌ Missing ElevenLabs credentials.")
        audio_cache[cache_key] = BytesIO(b"")
        return

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVEN_VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_API_KEY
    }
    payload = {
        "text": text,
        # model_id can be omitted if your ElevenLabs account uses default model,
        # or set to "eleven_multilingual_v2" if available to you.
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.6,
            "similarity_boost": 0.9,
            # You can tune style or other params here if supported for your voice.
        }
    }

    try:
        # Request MP3 bytes
        resp = requests.post(url, headers=headers, json=payload, stream=True, timeout=120)
        resp.raise_for_status()
        # read all bytes (ElevenLabs returns the full audio in response)
        audio_bytes = resp.content
        audio_cache[cache_key] = BytesIO(audio_bytes)
        print("✅ Voice cached for:", cache_key)
    except Exception as e:
        print("❌ ElevenLabs error:", e)
        audio_cache[cache_key] = BytesIO(b"")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(force=True) or {}
    question = (data.get("question") or "").strip()

    if not question:
        return jsonify({"error": "Empty question"}), 400

    # Retrieve similar docs from ChromaDB
    try:
        results = collection.query(query_texts=[question], n_results=5)
        docs = results["documents"][0]
    except Exception as e:
        print("❌ ChromaDB query error:", e)
        docs = []

    if not any(docs):
        fallback = "Beloved seeker, no wisdom rises now. Sit in stillness, and the answer shall come."
        synthesize_voice(fallback, "fallback")
        return jsonify({"answer": fallback, "audio_key": "fallback"})

    context = "\n\n".join(docs)

    system_prompt = (
        "You are Swami Anahata, a serene, poetic Tantric teacher.\n"
        "Respond in exactly 3 to 4 poetic lines, calm and reflective.\n"
        "Begin with 'Dear one,' or 'Beloved seeker,' and end with a sacred blessing.\n"
        "Use spiritual, Yogic language. Only use the given context from Vigyan Bhairav Tantra.\n"
    )

    user_prompt = f"""Context from Vigyan Bhairav Tantra:
{context}

Question: {question}

Please answer briefly in 3 to 4 poetic lines only.

Swami Anahata:"""

    try:
        # Call OpenRouter (Chat Completions)
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/mistral-7b-instruct",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.6,
                "max_tokens": 250
            },
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        answer = result["choices"][0]["message"]["content"].strip()
        cache_key = f"audio_{abs(hash(answer))}"

        print("🔮 Answer:", answer)
        # Convert answer to speech and cache it
        synthesize_voice(answer, cache_key)

        return jsonify({
            "answer": answer,
            "audio_key": cache_key
        })
    except Exception as e:
        print("❌ Failed to generate answer:", e)
        fallback = "Dear one, the energies are quiet. Please return in stillness and ask again."
        synthesize_voice(fallback, "fallback")
        return jsonify({"answer": fallback, "audio_key": "fallback"})

@app.route("/speak/<audio_key>")
def speak(audio_key):
    audio = audio_cache.get(audio_key)
    if audio:
        audio.seek(0)
        return send_file(audio, mimetype="audio/mpeg")
    return "Audio not found", 404

if __name__ == "__main__":
    # Run on 127.0.0.1:5000 for local dev
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
