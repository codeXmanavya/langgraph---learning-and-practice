import React from 'react'
import Chat_Message from './Chat_Message'
import { useEffect, useRef } from 'react';

const Chat_Window = ({messages}) => {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({behavior : 'smooth'})
  }, [messages]);


  return (
    <div className='flex-1 flex flex-col overflow-hidden bg-white mx-4 rounded-t-lg shadow-lg'>
      <div className='flex-1 overflow-y-auto p-4 space-y-2 bg-gray-50'>
        {messages.length === 0 ? (
          <div className='flex items-center justify-center h-full text-gray-500'>
            <div className='text-center'>
              <div className='text-6xl mb-4'>💬</div>
              <p className='text-lg font-medium'>Start a conversation</p>
              <p className='text-sm'>Type a message below to begin chatting with the AI</p>
            </div>
          </div>
        ) : (
          messages.map((msg, index) => (
            <Chat_Message key={index} text={msg.text} sender={msg.sender} />
          ))
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}

export default Chat_Window