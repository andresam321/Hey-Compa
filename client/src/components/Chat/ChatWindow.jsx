import React from "react";
import { useSelector } from "react-redux";

const ChatWindow = () => {
  const user = useSelector((state) => state.session.user);
  console.log("line7", user);

  return (
    <div className="max-h-screen w-full flex justify-center bg-gray-100 overflow-hidden">
      <div className="flex flex-col w-full max-w-2xl px-4 py-6">
        {/* Header */}
        <div className="mb-6 text-center">
          <h1 className="text-2xl font-bold text-gray-800">Hey</h1>
          <h2 className="text-lg text-gray-600">
            Compa {user?.firstname || "User"} 👋
          </h2>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto space-y-4 mb-4">
          <div className="bg-gray-200 text-gray-800 rounded-lg px-4 py-2 max-w-[75%] self-start">
            Hola Compa, ¿cómo estás?
          </div>
          <div className="bg-blue-600 text-white rounded-lg px-4 py-2 max-w-[75%] self-end ml-auto">
            Todo bien, ¿y tú?
          </div>
        </div>

        {/* Input */}
        <div className="flex items-center gap-2">
          <input
            type="text"
            placeholder="Type your message..."
            className="flex-1 rounded-full px-4 py-2 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button className="bg-blue-600 text-white px-4 py-2 rounded-full hover:bg-blue-700">
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;
