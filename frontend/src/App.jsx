import React, { useState } from "react";

export default function App() {
  const [question, setQuestion] = useState("");
  const [answerText, setAnswerText] = useState("Dear one, I am listening...");
  const [isLoading, setIsLoading] = useState(false);
  const [audio, setAudio] = useState(null);

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

      const answer = res.headers.get("X-Answer-Text");
      const audioBlob = await res.blob();
      const audioUrl = URL.createObjectURL(audioBlob);

      setAnswerText(answer);
      setAudio(audioUrl);
      const audioObj = new Audio(audioUrl);
      audioObj.play();
    } catch (err) {
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
        <img src="/swami.png" alt="Swami Logo" className="logo" />
        <h1>Swami Anahata </h1>
      </div>

      {/* Answer Box */}
      <div className="answer-box">
        {isLoading ? "Swami is reflecting..." : answerText}
      </div>

      {/* Question Box */}
      <div className="question-section">
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask your question..."
        />
        <button onClick={askSwami}>Ask Swami 🧘</button>
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
