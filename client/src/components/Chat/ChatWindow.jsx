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
<div className="min-h-screen w-full bg-slate-800 flex items-center justify-center">
  <div
    className={`w-full max-w-2xl transition-all duration-300 ease-in-out ${
      vendor ? "h-[85vh] rounded-lg" : "h-[400px] rounded-2xl"
    } bg-slate-700 shadow-2xl flex flex-col overflow-hidden`}
  >

    {!vendor && (
      <div className="flex-1 flex flex-col items-center justify-center text-center px-6">
        <h1 className="text-3xl font-semibold text-white mb-2">
          Hey Compa {user?.firstname || "User"} 👋
        </h1>
        <p className="text-gray-300 text-sm">
          Need help with a bill? Upload it below.
        </p>
      </div>
    )}


    {vendor && (
      <div className="flex-1 overflow-y-auto px-4 py-4 bg-[#1f1f27] space-y-4">
        <StartOcrSteps vendor={vendor} key={vendor} />
      </div>
    )}
    {/* Upload Always Visible */}
    <div className="border-t border-[#3d3d45] px-4 py-3 bg-[#2a2a32]">
      <UploadImage setVendor={setVendor} />
    </div>
  </div>
</div>
  );
};

export default ChatWindow;
