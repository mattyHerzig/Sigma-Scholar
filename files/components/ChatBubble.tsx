import React from 'react'
import Image from 'next/image'

interface ChatBubbleProps {
    text?: string;
    isUser: boolean;
    isLoading?: boolean;
    isScholarship?: boolean;
}

const ChatBubble: React.FC<ChatBubbleProps> = ({ text, isUser, isLoading, isScholarship}) => {
    return (
        <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} py-1 lg:px-20`}>
            {!isUser && <Image src='/counselor.png' width={32} height={32} alt="AI" className="h-8 w-8 rounded-full mr-2" />}
            <div className={`p-3 ${isUser ? 'rounded-l-lg rounded-br-lg rounded-bl-lg' : 'rounded-r-lg rounded-bl-lg rounded-br-lg'} ${isUser ? 'bg-blue-500' : 'bg-gray-400'} max-w-xs`}>
                {isLoading ? (
                    <div className="flex space-x-2 animate-pulse">
                        <div className="h-4 w-4 bg-gray-500 rounded-full"></div>
                        <div className="h-4 w-4 bg-gray-500 rounded-full"></div>
                        <div className="h-4 w-4 bg-gray-500 rounded-full"></div>
                    </div>
                ) : (
                    <p className="text-white">{text}</p>
                )}
                <div className={`${isUser ? 'right-0' : 'left-0'} absolute mb-2 w-3 h-3`}>
                    <svg className={`${isUser ? 'transform rotate-45' : 'transform -rotate-45'} fill-current text-white`} viewBox="0 0 12 12">
                        <polygon points="9 0 12 0 12 3"></polygon>
                    </svg>
                </div>
            </div>
            {isUser && <Image src='/default_user.png' width={32} height={32} alt="User" className="h-8 w-8 rounded-full ml-2" />}
        </div>
    )
}

export default ChatBubble;