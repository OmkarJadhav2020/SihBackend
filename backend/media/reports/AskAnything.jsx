import React, { useState, useEffect } from "react";
import "./askAnything.css"; // Import the CSS for styling
import axios from "axios";
const questions = [
  { id: 1, question: "How to upload a file through the panel?" },
  { id: 2, question: "Process for audit." },
  { id: 3, question: "How to find out current expenses with all details?" },
  { id: 4, question: "Final review checklist" },
];

const AskAnything = () => {
  const [selectedQuestion, setSelectedQuestion] = useState(null);
  const [userResponse, setUserResponse] = useState("");
  const [chatHistory, setChatHistory] = useState([]); // To store the chat history

  // This effect will run when the component mounts
  useEffect(() => {
    // Simulate a bot message
    setChatHistory([{ sender: "bot", message: "Hi!" }]);
  }, []);

  const handleQuestionSelect = (question) => {
    setSelectedQuestion(question);
    setUserResponse(""); // Reset user response when a new question is selected
  };

  const handleUserResponseChange = (e) => {
    setUserResponse(e.target.value);
  };

  const handleSendResponse = () => {
    if (!userResponse.trim()) return;

    // Append the user's response to the chat history
    setChatHistory((prev) => [
      ...prev,
      { sender: "user", message: userResponse },
    ]);

    setTimeout(async () => {
      const botResponse = {
        sender: "bot",
        message: "Processing your request...",
      };
      setChatHistory((prev) => [...prev, botResponse]);

      try {
        const response = await axios.post(
          `http://127.0.0.1:5000/ask_question`,
          { question: userResponse }
        );
        botResponse.message = response.data.answer;
        console.log(botResponse)
      } catch (error) {
        botResponse.message =
          "Sorry, there was an error processing your request.";
      }
      
      setChatHistory((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = botResponse; // Replace placeholder with actual response
        return updated;
      });
    }, 500);

    setUserResponse(""); // Clear the input box
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSendResponse();
    }
  };

  return (
    <div className="container_ask">
      {/* Header Section */}
      <div className="header">
        <h1>
          Hello, <span className="highlight">Investigator!</span>
        </h1>
        <p>How can I help you today?</p>
      </div>

      {/* Question Cards */}
      <div className="cards">
        {questions.map((item) => (
          <div
            key={item.id}
            className="card"
            onClick={() => handleQuestionSelect(item.question)}
          >
            <p className="card-text">{item.question}</p>
          </div>
        ))}
      </div>

      {/* Chat Response */}
      {selectedQuestion && (
        <div className="chat-response">
          <div className="question">
            <div className="bubble">Q</div>
            <p>{selectedQuestion}</p>
          </div>
          <div className="answer">
            <div className="star-icon">★</div>
            <p className="answer-text">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut enim
              ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
              aliquip ex ea commodo consequat.
            </p>
          </div>
        </div>
      )}

      {/* Chat History */}
      <div className="chat">
        {chatHistory.map((chat, index) => (
          <div
            key={index}
            className={`chat-bubble ${chat.sender === "bot" ? "bot" : "user"}`}
          >
            <p
              className={`${
                chat.sender === "bot" ? "chat-user-bot" : "chat-user-msg"
              }`}
            >
              {chat.message}
            </p>
          </div>
        ))}
      </div>

      {/* Typing Box */}
      <div className="typing-box">
        <input
          className="input-box"
          value={userResponse}
          onChange={handleUserResponseChange}
          onKeyPress={handleKeyPress}
          placeholder="Start typing here..."
        />
      </div>
    </div>
  );
};

export default AskAnything;
