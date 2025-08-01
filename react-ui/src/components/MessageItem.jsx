import React from 'react';

export default function MessageItem({ message, isUser }) {
    return (
        <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-3`}>
            <div
                className={`max-w-[70%] p-3 rounded-2xl shadow ${isUser
                        ? 'bg-blue-500 text-white rounded-br-none'
                        : 'bg-gray-100 text-gray-800 rounded-bl-none'
                    }`}
            >
                {message}
            </div>
        </div>
    );
}