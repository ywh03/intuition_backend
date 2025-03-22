// src/components/ChatbotInterface.js
import React, { useState } from 'react';

function ChatbotInterface() {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hello, this is ShiftSense! How can I help you?' },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isFullScreen, setIsFullScreen] = useState(false);
  const [selectedFramework, setSelectedFramework] = useState("ADKAR");

  const frameworks = [
    "Kotter's 8-Step",
    "ADKAR",
    "Lewin's Change Model",
    "McKinsey 7S",
    "Prosci"
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const userMessage = { sender: 'user', text: inputValue.trim() };
    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');

    if (messages.length === 1) {
      setIsFullScreen(true);
    }

    const typingMessage = { sender: 'bot', text: '...' };
    setMessages((prev) => [...prev, typingMessage]);

    const controller = new AbortController();
    const timeout = setTimeout(() => {
      controller.abort();
    }, 40000); // 40 seconds

    try {
      const response = await fetch("http://localhost:8000/decide-framework", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: inputValue.trim() }),
        signal: controller.signal,
      });

      clearTimeout(timeout);
      const data = await response.json();

      setMessages((prev) => {
        const updated = [...prev];
        const lastIndex = updated.length - 1;
        if (updated[lastIndex]?.text === '...') {
          updated.splice(lastIndex, 1);
        }

        return [
          ...updated,
          {
            sender: 'bot',
            text: `💡 *Recommended Model:* ${data.model}\n\n*Answer:* ${data.answer}\n\n*Why:* ${data.justification}`,
          },
        ];
      });

    } catch (error) {
      setMessages((prev) => {
        const updated = [...prev];
        updated.pop();
        return [
          ...updated,
          { sender: 'bot', text: error.name === "AbortError" ? 'Request timed out after 40 seconds.' : 'Failed to get response.' },
        ];
      });
    }
  };

  const handleExit = () => {
    setIsFullScreen(false);
  };

  const containerStyle = {
    ...styles.chatContainer,
    ...(isFullScreen ? styles.fullScreenContainer : styles.smallContainer),
  };

  if (isFullScreen) {
    return (
      <div style={containerStyle}>
        <button style={styles.exitButton} onClick={handleExit}>
          ✕
        </button>

        <div style={styles.fullScreenLayout}>
          <div style={styles.sidePanel}>
            <h3 style={styles.panelHeader}>Select Framework</h3>
            <ul style={styles.frameworkList}>
              {frameworks.map((framework) => (
                <li
                  key={framework}
                  style={
                    selectedFramework === framework
                      ? styles.selectedFramework
                      : styles.frameworkItem
                  }
                  onClick={() => setSelectedFramework(framework)}
                >
                  {framework}
                </li>
              ))}
            </ul>
          </div>
          <div style={styles.chatArea}>
            <div style={styles.messagesContainer}>
              {messages.map((msg, index) => (
                <div
                  key={index}
                  style={
                    msg.sender === 'user'
                      ? styles.userMessage
                      : styles.botMessage
                  }
                >
                  {msg.text}
                </div>
              ))}
            </div>
            <form onSubmit={handleSubmit} style={styles.form}>
              <input
                type="text"
                placeholder="Ask me anything..."
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                style={styles.input}
              />
              <button type="submit" style={styles.button}>
                Send
              </button>
            </form>
          </div>
        </div>
      </div>
    );
  } else {
    return (
      <div style={containerStyle}>
        <div style={styles.messagesContainer}>
          {messages.map((msg, index) => (
            <div
              key={index}
              style={msg.sender === 'user' ? styles.userMessage : styles.botMessage}
            >
              {msg.text}
            </div>
          ))}
        </div>
        <form onSubmit={handleSubmit} style={styles.form}>
          <input
            type="text"
            placeholder="Ask me anything..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            style={styles.input}
          />
          <button type="submit" style={styles.button}>
            Send
          </button>
        </form>
      </div>
    );
  }
}

const styles = {
  chatContainer: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    borderRadius: '10px',
    padding: '1rem',
    boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
    backgroundColor: '#fff',
    overflow: 'hidden',
  },
  smallContainer: {
    position: 'absolute',
    right: '5rem',
    top: '9rem',
    width: '400px',
    height: '547px',
    border: '1px solid #ccc',
    zIndex: 10,
  },
  fullScreenContainer: {
    position: 'fixed',
    top: 0,
    left: 0,
    width: '98vw',
    height: '98vh',
    border: 'none',
    zIndex: 9999,
  },
  exitButton: {
    position: 'absolute',
    top: '0.5rem',
    right: '0.5rem',
    background: 'transparent',
    border: 'none',
    fontSize: '1.5rem',
    cursor: 'pointer',
    color: '#333',
    zIndex: 10000,
  },
  fullScreenLayout: {
    display: 'flex',
    height: '100%',
  },
  sidePanel: {
    width: '300px',
    borderRight: '1px solid #ccc',
    padding: '1rem',
    backgroundColor: '#f1f1f1',
    overflowY: 'auto',
  },
  panelHeader: {
    margin: 0,
    marginBottom: '1rem',
  },
  frameworkList: {
    listStyleType: 'none',
    padding: 0,
  },
  frameworkItem: {
    padding: '0.5rem',
    cursor: 'pointer',
  },
  selectedFramework: {
    padding: '0.5rem',
    cursor: 'pointer',
    backgroundColor: '#007bff',
    color: '#fff',
    borderRadius: '4px',
  },
  chatArea: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    padding: '1rem',
  },
  messagesContainer: {
    overflowY: 'auto',
    flex: 1,
    marginBottom: '1rem',
  },
  userMessage: {
    backgroundColor: '#d4edda',
    padding: '0.5rem',
    borderRadius: '5px',
    margin: '0.5rem 0',
    alignSelf: 'flex-end',
  },
  botMessage: {
    backgroundColor: '#f8d7da',
    padding: '0.5rem',
    borderRadius: '5px',
    margin: '0.5rem 0',
    alignSelf: 'flex-start',
  },
  form: {
    display: 'flex',
  },
  input: {
    flex: 1,
    padding: '0.5rem',
    fontSize: '1rem',
  },
  button: {
    padding: '0.5rem 1rem',
    fontSize: '1rem',
    marginLeft: '0.5rem',
    backgroundColor: '#007bff',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
  },
};

export default ChatbotInterface;
