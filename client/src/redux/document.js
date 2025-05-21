import { fetchWithCSRF } from "../utils/fetchWithCSRF";
const DOCUMENT_UPLOAD_IMAGE = 'documentUploadImage/DOCUMENT_UPLOAD_IMAGE';



const docUploadImage = (image) => ({
  type: DOCUMENT_UPLOAD_IMAGE,
  payload: image,
});


export const thunkUploadImage = (image) => async (dispatch) => {
  try {
    const res = await fetchWithCSRF("/api/documents/image/upload", {
      method: "POST",
      body: image,
    });
    if (!res.ok) {
      throw new Error("Image upload failedk");
    }
    const data = await res.json();
    if (data.error) {
      throw new Error(data.error);
    }
    dispatch(docUploadImage(data.image));
    return data.image;
  } catch (error) {
    console.error("Error uploading image:", error);
    throw error;
  }
}


function documentReducer(state = {}, action) {
  switch (action.type) {
    case DOCUMENT_UPLOAD_IMAGE:
      return {
        ...state,
        image: action.payload,
      };
    default:
      return state;
  }
}

export default documentReducer;