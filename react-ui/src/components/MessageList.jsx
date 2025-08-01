import React from 'react';
import MessageItem from './MessageItem';

export default function MessageList({ messages, endRef }) {
    return (
        <div className="flex-1 overflow-y-auto p-6 bg-gray-50">
            {messages.map((msg, idx) => (
                <MessageItem key={idx} message={msg.text} isUser={msg.sender === 'user'} />
            ))}
            <div ref={endRef} />
        </div>
    );
}