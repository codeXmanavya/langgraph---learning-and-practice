import './App.css'
import Chat_Input from './components/Chat_Input'
import Chat_Window from './components/Chat_Window'
import { useState } from 'react'
// import chatbot from '../../backend/main.py'
// import { sendMessageToAgent } from './api';

function App() {
  const [chatMessage, setChatMessage] = useState([])

  const handleSend = async (text) => {``
    // add user message
    setChatMessage((prev) => [...prev, {text, sender:'user'}])

    // backend resonse from ai
 
  const response = await fetch("http://localhost:8000/", {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({text})
  });

  const data = await response.json();

    // add ai message
    setChatMessage((prev) => [...prev , {text: data.response, sender:'ai' }])
  }

  return (
    <div className='flex flex-col h-screen w-screen bg-gradient-to-br from-blue-50 to-indigo-100'>
      {/* Header */}
      <div className='bg-white shadow-sm border-b p-4 flex items-center justify-center'>
        <h1 className='text-2xl font-bold text-gray-800 flex items-center gap-2'>
          <div className='w-8 h-8 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full flex items-center justify-center'>
            <span className='text-white text-sm font-bold'>AI</span>
          </div>
          My ChatBot
        </h1>
      </div>
      
      {/* Chat Area */}
      <div className='flex-1 flex flex-col overflow-hidden'>
        < Chat_Window messages={chatMessage} />
        < Chat_Input onsend={handleSend} />
      </div>
    </div>
  )
}

export default App
