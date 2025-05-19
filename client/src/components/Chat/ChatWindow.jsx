import React from 'react'
import "../Styles/ChatWindow.css"
import { useSelector  } from 'react-redux';

const ChatWindow = () => {
    const user = useSelector((state) => state.session.user);
    console.log("line7", user)

  return (
    <div className="chat-page">
      <div className="chat-wrapper">
        <div className="chat-container">
          <div className="chat-header">
            <h1>Hey</h1>
            <h2>Compa {user.firstname} 👋</h2>
          </div>
          <div className="chat-messages">
            <div className="message compa"></div>
            <div className="message user"></div>
          </div>

          <div className="chat-input">
            <input type="text" placeholder="Type your message..." />
            <button>Send</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatWindow
