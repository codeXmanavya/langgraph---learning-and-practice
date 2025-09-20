import React from "react";
import { useState } from "react";

const Chat_Input = ({onsend}) => {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (input.trim() !== "") {
      onsend(input);
      setInput("");
    }
  };

  return (
    <div className="bg-white mx-4 mb-4 p-4 rounded-b-lg shadow-lg border-t border-gray-200">
      <div className="flex gap-3 items-end">
        <div className="flex-1">
          <input
            type="text"
            className="w-full border border-gray-300 rounded-xl px-4 py-3 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none transition-all duration-200 shadow-sm"
            value={input}
            placeholder="Type your message here..."
            onChange={(e) => {setInput(e.target.value)}}
            onKeyDown={(e) => e.key == 'Enter' && handleSend()}
          />
        </div>
        <button 
          className="px-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-xl hover:from-blue-600 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transform transition-all duration-200 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed shadow-md font-medium"
          onClick={handleSend}
          disabled={input.trim() === ""}
        >
          <span className="flex items-center gap-2">
            Send
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </span>
        </button>
      </div>
    </div>
  );
};

export default Chat_Input;
