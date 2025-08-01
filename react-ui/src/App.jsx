// src/App.jsx
import React, { useState, useRef, useEffect } from 'react';
import SelectDatabaseButton from './components/SelectDatabaseButton';
import MessageList from './components/MessageList';
import ChatInput from './components/ChatInput';

export default function App() {
  const [messages, setMessages] = useState([
    { text: 'Hello! How can I help you today?', sender: 'bot' }
  ]);
  const [input, setInput] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const thinkingTimeout = useRef(null);
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = () => {
    const text = input.trim();
    if (!text || isThinking) return;

    setMessages(prev => [...prev, { text, sender: 'user' }]);
    setInput('');
    setIsThinking(true);
    setMessages(prev => [...prev, { text: '🧠 Thinking...', sender: 'bot' }]);

    thinkingTimeout.current = setTimeout(() => {
      setMessages(prev => prev.filter(m => m.text !== '🧠 Thinking...'));
      setMessages(prev => [...prev, { text: `You said: ${text}`, sender: 'bot' }]);
      setIsThinking(false);
      thinkingTimeout.current = null;
    }, 2000);
  };

  const handleCancel = () => {
    if (thinkingTimeout.current) {
      clearTimeout(thinkingTimeout.current);
      thinkingTimeout.current = null;
      setIsThinking(false);
      setMessages(prev => prev.filter(m => m.text !== '🧠 Thinking...'));
    }
  };

  const handleSelectDatabase = () => {
    console.log('Select DuckDB database');
    // TODO: Open file selector modal
  };

  return (
    <div className="h-screen bg-gradient-to-b from-white to-gray-100 px-4">
      <div className="mx-auto flex flex-col w-full max-w-3xl h-full bg-white border border-gray-200 rounded-xl shadow-lg">
        <header className="flex items-center justify-between px-4 py-2 bg-white border-b border-gray-200">
          <SelectDatabaseButton onSelect={handleSelectDatabase} />
          <h1 className="text-lg font-semibold">DuckDB Chat</h1>
        </header>
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Scrollable messages */}
          <div className="flex-1 overflow-y-auto p-6 bg-gray-50">
            <MessageList messages={messages} endRef={endRef} />
          </div>
          {/* Sticky input */}
          <ChatInput
            input={input}
            onChange={setInput}
            onSend={handleSend}
            isThinking={isThinking}
            onCancel={handleCancel}
          />
        </div>
      </div>
    </div>
  );
}
