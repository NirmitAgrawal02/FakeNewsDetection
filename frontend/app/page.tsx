"use client";

import { useState } from 'react';
export default function Home() {
  const[text, newText] = useState('');
  const[news, setNews] = useState('');
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const response = await fetch('http://localhost:5000/check', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text }),
    });
    const data = await response.json();
    setNews(data.prediction);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
        <h1 className="text-2xl font-semibold mb-4">Fake News Detection</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Enter Fake or Real:
          <input
            type="text"
            value={text}
            onChange={(e) => newText(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded"
            required
            />
            </label>
            <button
            type="submit"
            className="w-full bg-blue-500 text-white p-2 rounded-md hover:bg-blue-600 transition"
          >
            Check News
          </button>
          </div>
          {news != null && (
            <p className="text-lg font-semibold mt-4">
              Result: {news}
            </p>
          )}
        </form>
          
    </div>
    </div>
  );
}
