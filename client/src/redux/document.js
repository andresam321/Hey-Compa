import { fetchWithCSRF } from "../utils/fetchWithCSRF";
const DOCUMENT_UPLOAD_IMAGE = 'documentUploadImage/DOCUMENT_UPLOAD_IMAGE';



const docUploadImage = (image) => ({
  type: DOCUMENT_UPLOAD_IMAGE,
  payload: image,
});

// const res = await fetch("/api/documents/ping")
// const data = await res.json()
// console.log("Ping response:", data);


export const thunkUploadImage = (image) => async (dispatch) => {
  try {
    const res = await fetchWithCSRF("/api/documents/image/upload", {
      method: "POST",
      body: image,
      // credentials: "include", // if you're using session auth
    });
    if (!res.ok) {
      throw new Error("Image upload failedk");
    }
    const data = await res.json();
    console.log("Image upload response:", data);
      if (data.error) {
        throw new Error(data.error);
      }
      dispatch(docUploadImage(data));
      console.log("Image uploaded successfully:", data);
      return data;
  } catch (error) {
    console.error("Error uploading image:", error);
    throw error;
  }
}


function documentReducer(state = {}, action) {
  switch (action.type) {
    case DOCUMENT_UPLOAD_IMAGE:{
      console.log("Image upload action:", action);
      console.log("Image upload state:", state);
      console.log("Image upload payload:", action.payload);
      const newState = { ...state };
            newState[action.payload.id] = action.payload
            return newState
        }

    default:
      return state;
  }
}

export default documentReducer;