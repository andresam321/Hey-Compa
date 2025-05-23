import { fetchWithCSRF } from "../utils/fetchWithCSRF";

const GET_PAYMENT_GUIDE = 'paymentGuide/GET_PAYMENT_GUIDE';

const getPaymentGuide = (paymentGuide) => ({
  type: GET_PAYMENT_GUIDE,
  payload: paymentGuide,
}); 

export const thunkGetPaymentGuide = (vendor) => async (dispatch) => {
    try {
    const encodedVendor = encodeURIComponent(vendor);
    const res = await fetchWithCSRF(`/api/payment_guide/${encodedVendor}`);
    if (!res.ok) {
        throw new Error("Failed to fetch payment guide");
    }
    const data = await res.json();
    if (data.error) {
        throw new Error(data.error);
    }
        dispatch(getPaymentGuide(data));
        return data;
    } catch (error) {
        console.error("Error fetching payment guide:", error);
        throw error;
    }
}

function paymentGuideReducer(state = {}, action) {
  switch (action.type) {
    case GET_PAYMENT_GUIDE:
      return {
        ...state,
        paymentGuide: action.payload,
      };
    default:
      return state;
  }
}


export default paymentGuideReducer;