import React from 'react';

export default function SelectDatabaseButton({ onSelect }) {
    return (
        <button
            className="px-4 py-2 rounded-lg border border-gray-300 bg-white hover:bg-gray-50 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
            onClick={onSelect}
        >
            Select Database
        </button>
    );
}