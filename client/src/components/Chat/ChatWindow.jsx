import {useState} from "react";
import { useSelector } from "react-redux";
import UploadImage from "../Documents/UploadImage";
import StartOcrSteps from "../GuideSteps/StartOcrSteps";
import OpenModalButton from "../OpenModalButton/OpenModalButton";

const ChatWindow = () => {
  const user = useSelector((state) => state.session.user);
  const [vendor, setVendor] = useState(null);

  console.log("line7", user);

const handleFileUpload = (e) => {
  alert("File uploader");
};


  return (
<div className="min-h-screen w-full bg-[#1e1e2f] flex justify-center">
  <div className="w-full max-w-5xl flex flex-col px-6 py-8">

    {/* Header */}
    <div className="mb-6 text-center">
      <h1 className="text-3xl font-bold text-white">Hey Compa {user?.firstname || "User"} 👋</h1>
    </div>

      <div className="flex-1 bg-white rounded-lg shadow-md p-6 overflow-y-auto space-y-4 mb-6 min-h-[400px]">
      <div className="bg-gray-200 text-gray-800 rounded-lg px-4 py-2 max-w-[75%]">
        Need help with a bill? Try uploading it here!
      </div>

      {vendor && (
        <div className="bg-gray-200 text-gray-800 rounded-lg px-4 py-2 max-w-[75%] self-start">
          <StartOcrSteps vendor={vendor} key={vendor} />
        </div>
      )}
    </div>

    <div className="...">
      <UploadImage setVendor={setVendor} />
    </div>


  </div>
</div>
  );
};

export default ChatWindow;
