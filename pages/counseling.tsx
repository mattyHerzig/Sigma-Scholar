import React, { FormEvent, useState } from 'react';
import ChatBubble from '../components/ChatBubble';

interface MessageProps {
  text?: string;
  isUser: boolean;
  isLoading?: boolean;
  isScholarship?: boolean;
}

export default function Counseling() {
  const [messages, setMessages] = useState<MessageProps[]>([]);
  const [inputValue, setInputValue] = useState<string>('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleSentMessage = async (e: FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim()) return;
    setMessages([...messages, { text: inputValue, isUser: true }]);
    setInputValue('');
    try {
      await handleSubmit(inputValue);
    } catch (er) {
      console.log(er);
    }
  };

  const handleSubmit = async (query: any) => {
    try {
      setMessages(prevMessages => [
        ...prevMessages,
        { text: query, isLoading: true, isUser: false } // Assuming the response is from AI, not the user
      ]);
      const response = await fetch("/api/data", {
        method: 'POST',
        headers: {
          'Content-Type':'application/json'
        },
        body: JSON.stringify({'message':query})
      });

      const data = await response.json();
      const { message } = data;
      console.log('mario', message);
      setMessages(prevMessages => prevMessages.slice(0, -1));
      setMessages(prevMessages => [
        ...prevMessages,
        { text: message, isLoading: false, isUser: false } // Assuming the response is from AI, not the user
      ]);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div className='flex flex-col min-h-screen overflow-hidden'>
      <div className='p-5 flex-grow overflow-y-auto'>
        <ChatBubble text="Hello, how can I help you?" isUser={false} />
        {messages.map((message, index) => (
          <div key={index} className="animate-slideIn">
            <ChatBubble text={message.text} isLoading={message.isLoading} isUser={message.isUser} />
          </div>
        ))}
      </div>
      <form className="w-full fixed bottom-0 flex items-center justify-center" onSubmit={handleSentMessage}>
        <input
          type="search"
          placeholder="Chat with an AI counselor..."
          onChange={handleInputChange}
          value={inputValue}
          className="w-7/12 rounded-full border-2 border-gray-200 mb-4 focus:outline-none shadow-xl p-4"
        />
      </form>
    </div>
  );
}
