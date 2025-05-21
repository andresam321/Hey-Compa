import {useState} from "react";
import { useSelector } from "react-redux";
import UploadImage from "../Documents/UploadImage";
import OpenModalButton from "../OpenModalButton/OpenModalButton";

const ChatWindow = () => {
  const user = useSelector((state) => state.session.user);
  console.log("line7", user);

const handleFileUpload = (e) => {
  alert("File uploader");
};


  return (
    <div className="max-h-screen w-full flex justify-center bg-gray-100 overflow-hidden">
      <div className="flex flex-col w-full max-w-2xl px-4 py-6">
        {/* Header */}
        <div className="mb-6 text-center">
          <h1 className="text-2xl font-bold text-gray-800">Hey Compa {user?.firstname || "User"} 👋 </h1>
          {/* <h2 className="text-lg text-gray-600">
            Compa {user?.firstname || "User"} 👋
          </h2> */}
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto space-y-4 mb-4">
          <div className="bg-gray-200 text-gray-800 rounded-lg px-4 py-2 max-w-[75%] self-start">
            Need help with a bill? Try uploading it here!
          </div>
        </div>

        {/* Input */}
        <div className="flex items-center justify-between gap-4">
          <div>
            <OpenModalButton
                buttonText={"Upload Image"}
                className="view-details-button"
                modalComponent={<UploadImage />}
            />
        </div>
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;
