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

    try {
      const res = await fetch("http://localhost:5000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      const data = await res.json();
      console.log("📥 Data from backend:", data);

      if (data.answer && data.audio_key) {
        setAnswerText(data.answer); // ✅ Set text properly

        const audioUrl = `http://localhost:5000/speak/${data.audio_key}`;
        const audio = new Audio(audioUrl);
        setIsSpeaking(true);
        audio.play();
        audio.onended = () => setIsSpeaking(false);
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
    <div className="chat-container">
      {/* Logo Header */}
      <div className="header">
        <img src="/swami.jpg" alt="Swami Logo" className="logo" />
        <h1>Swami Anahata</h1>
      </div>

      {/* Answer Box */}
      <div className="answer-box">
        <p>{answerText}</p>
        {isSpeaking && <p>🔊 Swami is speaking...</p>}
      </div>

      {/* Question Box */}
      <div className="question-section">
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask your question..."
        />
        <button onClick={askSwami} disabled={isLoading}>
          {isLoading ? "Reflecting..." : "Ask Swami 🧘"}
        </button>
      </div>

      {/* Footer with spiritual quote */}
      <footer className="footer">
        “Truth is not found in books, but in breath.”
        <br />
        <span className="footer-credit">— Swami Anahata</span>
      </footer>
    </div>
  );
}
