// app.jsx
import React, { useState } from "react";

export default function App() {
  const [question, setQuestion] = useState("");
  const [answerText, setAnswerText] = useState("Dear one, I am listening...");
  const [isLoading, setIsLoading] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);

  const askSwami = async () => {
    if (!question.trim()) return;

    setIsLoading(true);
    setAnswerText("Swami is contemplating...");
    setIsSpeaking(false);

    try {
      const res = await fetch("http://127.0.0.1:5000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }

      const data = await res.json();
      console.log("📥 Data from backend:", data);

      if (data.answer && data.audio_key) {
        setAnswerText(data.answer);

        // Play cached MP3 from server
        const audioUrl = `http://127.0.0.1:5000/speak/${data.audio_key}`;
        const audio = new Audio(audioUrl);
        audio.preload = "auto";
        setIsSpeaking(true);
        audio.play().catch((err) => {
          console.error("Audio play failed:", err);
          setIsSpeaking(false);
        });
        audio.onended = () => setIsSpeaking(false);
        audio.onerror = (e) => {
          console.error("Audio error:", e);
          setIsSpeaking(false);
        };
      } else {
        setAnswerText("Dear one, Swami did not respond this time.");
      }
    } catch (err) {
      console.error("❌ Error:", err);
      setAnswerText("Dear one, something divine went silent. Please try again.");
    } finally {
      setIsLoading(false);
      setQuestion("");
    }
  };

  return (
    <div className="chat-container" style={{ maxWidth: 720, margin: "2rem auto", fontFamily: "serif" }}>
      <div className="header" style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <img src="/swami.jpg" alt="Swami Logo" className="logo" style={{ width: 64, height: 64, borderRadius: 8 }} />
        <h1>Swami Anahata</h1>
      </div>

      <div className="answer-box" style={{ border: "1px solid #ddd", padding: 20, borderRadius: 8, marginTop: 20 }}>
        <p style={{ whiteSpace: "pre-wrap" }}>{answerText}</p>
        {isSpeaking && <p>🔊 Swami is speaking...</p>}
      </div>

      <div className="question-section" style={{ marginTop: 16 }}>
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask your question..."
          rows={4}
          style={{ width: "100%", padding: 12, borderRadius: 8, fontSize: 16 }}
        />
        <button
          onClick={askSwami}
          disabled={isLoading || !question.trim()}
          style={{ marginTop: 8, padding: "10px 16px", borderRadius: 8, cursor: isLoading ? "not-allowed" : "pointer" }}
        >
          {isLoading ? "Reflecting..." : "Ask Swami 🧘"}
        </button>
      </div>

      <footer className="footer" style={{ marginTop: 24, color: "#666" }}>
        “Truth is not found in books, but in breath.” <br />
        <span className="footer-credit">— Swami Anahata</span>
      </footer>
    </div>
  );
}
