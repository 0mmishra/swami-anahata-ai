# 🧘‍♂️ Swami Anahata - Spiritual AI Voice Assistant

A serene AI chatbot inspired by **Swami Anahata**, trained on the sacred teachings of the **Vigyan Bhairav Tantra**, Swami's Instagram/Youtube content, and spiritual insights. This assistant delivers calm, poetic, 3–4 line spoken answers in Swami's voice using AI technologies.

---

## 🌟 Features

- 💬 **Ask Spiritual Questions** based on Vigyan Bhairav Tantra.
- 🧠 Uses **ChromaDB** for contextual vector search over embedded spiritual data.
- 🧘‍♂️ Responds in **Swami Anahata's tone** — calm, poetic, meditative.
- 🔊 **Text-to-speech (TTS)** voice output using OpenAI's `onyx` voice (close match to Swami’s speech).
- 🎤 Custom-trained on Swami's social media content (YouTube & Instagram).
- 🌐 Built with **React** frontend and **Flask** backend.

---

## 🧱 Tech Stack

| Layer        | Tech Used                                   |
|--------------|---------------------------------------------|
| Frontend     | React + Tailwind + Animations               |
| Backend      | Python (Flask) + ChromaDB                   |
| AI API       | OpenRouter (Mixtral 7B via mistral-7b-instruct) |
| Voice        | OpenAI TTS API (`onyx` voice model)         |
| Embeddings   | `sentence-transformers` (MiniLM-L6-v2)       |

---

## 📁 Data Sources

The assistant responds based on:

1. 📜 **Vigyan Bhairav Tantra**: Uploaded PDF converted into vector embeddings.
2. 📺 **Swami Anahata's YouTube Content**: Transcripts from talks scraped and embedded.
3. 📸 **Swami’s Instagram Posts**: Captions and quotes embedded into ChromaDB.

All data is embedded using `all-MiniLM-L6-v2` and stored inside a persistent **ChromaDB** database (`/anahata_db` folder).

---

## 🚀 How to Run

2. Backend Setup

cd server
pip install -r requirements.txt

3. Create a .env file:

OPENROUTER_API_KEY=your_openrouter_api_key
OPENAI_API_KEY=your_openai_api_key

4. Start the Flask server:

python server.py

5. Frontend Setup

cd frontend
npm install
npm run dev

📦 Folder Structure

ahanta/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── swami.png
│   └── index.html
├── server/
│   ├── server.py
│   ├── .env
│   ├── requirements.txt
│   └── anahata_db/       ✅ your ChromaDB folder
├── README.md             ✅ full documentation
└── any other files used


🧘 Sample Prompt Examples
“What is the nature of the Self?”

“How can I become more meditative in chaos?”

“Explain breath awareness from Tantra.”

💡 Response will come in 3–4 poetic lines, beginning with "Dear one," and ending in a spiritual blessing.

🛡️ Disclaimer
This assistant is a spiritual guide inspired by Swami Anahata's tone and teachings. It is for meditative, reflective purposes and does not replace real spiritual practice or personal guidance

