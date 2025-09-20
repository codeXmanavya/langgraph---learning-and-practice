import React from 'react'

const Chat_Message = ({text,sender}) => {
  return (
    <div className={`flex ${sender === 'user' ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`max-w-xs lg:max-w-md xl:max-w-lg px-4 py-3 rounded-2xl shadow-md ${
        sender === 'user' 
          ? 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-br-md' 
          : 'bg-white text-gray-800 border border-gray-200 rounded-bl-md'
      }`}>
        <div className="text-sm font-medium leading-relaxed">
          {text}
        </div>
        {sender === 'ai' && (
          <div className="flex items-center mt-2 text-xs text-gray-500">
            <div className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></div>
            AI Assistant
          </div>
        )}
      </div>
    </div>
  )
};

export default React.memo(Chat_Message)