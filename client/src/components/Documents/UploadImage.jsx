import {useState, useEffect} from 'react'
import { useSelector } from 'react-redux'
import { useDispatch } from 'react-redux'
import { thunkUploadImage } from '../../redux/document'

const UploadImage = () => {
  const navigate = useDispatch();
  const dispatch = useDispatch();
  const [image, setImage] = useState();
  const [showImage, setShowImage] = useState();
  const [error, setError] = useState({});
  const [fileName, setFileName] = useState("");
  
  const handleFileChange = (e) => {
        const file = e.target.files[0];
        setImage(file);
        setShowImage(URL.createObjectURL(file));
        setFileName(file.name || "");
        if (file) {
            const reader = new FileReader();
            reader.onload = () => {
                setShowImage(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };
  const handleUpload = async (e) => {
    e.preventDefault();
    setError({});

    if (!image) {
      setError({ image: "Please select an image to upload." });
      return;
    }

    const formData = new FormData();
    formData.append("image", image);

    try {
      const uploadedImage = await dispatch(thunkUploadImage(formData));
      console.log("Uploaded Image:", uploadedImage);
      setImage(null);
      setShowImage(null);
      setFileName("");
      // Handle success (e.g., show a success message or navigate)
    } catch (error) {
      console.error("Error uploading image:", error);
      setError({ image: "Image upload failed. Please try again." });
    }
  }

  return (
    <div>
      <div>
        <h1 className="text-2xl font-bold text-gray-800">Upload Image</h1>
        <form onSubmit={handleUpload} className="flex flex-col gap-4">
          <label className="flex items-center bg-white border border-gray-300 rounded-full px-4 py-2 cursor-pointer hover:bg-gray-50 text-gray-600">
            📎 Upload an image
            <input
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              className="hidden"
            />
            {showImage && (
                <div className="mt-2">
                  <img src={showImage} alt="Preview" width="100" className="mb-1 rounded" />
                  <p className="text-sm text-gray-500">{fileName}</p>
                </div>
              )}
          </label>
          {error.image && <p className="text-red-500">{error.image}</p>}
          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded-full hover:bg-blue-700"
          >
            Submit
          </button>
        </form>
      </div>
    </div>
  )
}

export default UploadImage
