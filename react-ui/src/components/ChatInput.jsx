import React from 'react';

export default function ChatInput({ input, onChange, onSend, isThinking, onCancel }) {
    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            isThinking ? onCancel() : onSend();
        }
    };

    // Define a consistent palette: Indigo for send, Red for stop
    const sendClasses = 'bg-indigo-600 hover:bg-indigo-700 focus:ring-indigo-500';
    const stopClasses = 'bg-red-600 hover:bg-red-700 focus:ring-red-500';

    return (
        <div className="p-4 border-t border-gray-200 flex items-center bg-white">
            <textarea
                className="flex-1 px-4 py-2 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none h-12"
                value={input}
                onChange={e => onChange(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type your message..."
            />
            <button
                onClick={isThinking ? onCancel : onSend}
                className={`ml-2 p-2 rounded-r-lg focus:outline-none focus:ring-2 shadow flex items-center justify-center text-white ${isThinking ? stopClasses : sendClasses
                    }`}
            >
                {isThinking ? (
                    /* Stop icon */
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 fill-white" viewBox="0 0 24 24">
                        <rect x="6" y="6" width="12" height="12" />
                    </svg>
                ) : (
                    /* Send icon */
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 fill-white" viewBox="0 0 24 24">
                        <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
                    </svg>
                )}
            </button>
        </div>
    );
}