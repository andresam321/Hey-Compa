import { fetchWithCSRF } from "../utils/fetchWithCSRF";

const GET_GUIDE_STEP_PROGRESS = 'guideProgress/GET_GUIDE_STEP_PROGRESS';
const NEXT_STEP_GUIDE_PROGRESS = 'guideProgress/NEXT_STEP_GUIDE_PROGRESS';
const REPEAT_STUCK_GUIDE_PROGRESS = 'guideProgress/REPEAT_STUCK_GUIDE_PROGRESS';

// Action creators
const getGuideStepProgress = (guideStepProgress) => ({
  type: GET_GUIDE_STEP_PROGRESS,
  payload: guideStepProgress,
});
const nextStepGuideProgress = (guideStepProgress) => ({
  type: NEXT_STEP_GUIDE_PROGRESS,
  payload: guideStepProgress,
});
const repeatStuckGuideProgress = (guideStepProgress) => ({
  type: REPEAT_STUCK_GUIDE_PROGRESS,
  payload: guideStepProgress,
});
// Thunk action creators
//dispatch thunk to get guide step progress
export const thunkGetGuideStepProgress = (vendor) => async (dispatch) => {
  try {
    const res = await fetchWithCSRF(`/api/guide_progress/start/${vendor}`);
    if (!res.ok) {
      throw new Error("Failed to fetch guide step progress");
    }
    const data = await res.json();
    if (data.error) {
      throw new Error(data.error);
    }
    dispatch(getGuideStepProgress(data));
    return data;
  } catch (error) {
    console.error("Error fetching guide step progress:", error);
    throw error;
  }
}

//dispatch thunk to get next step guide progress
export const thunkNextStepGuideProgress = (vendor) => async (dispatch) => {
  try {
    const res = await fetchWithCSRF(`/api/guide_progress/next/${vendor}`);
    if (!res.ok) {
      throw new Error("Failed to fetch guide step progress");
    }
    const data = await res.json();
    if (data.error) {
      throw new Error(data.error);
    }
    dispatch(nextStepGuideProgress(data));
    return data;
  } catch (error) {
    console.error("Error fetching guide step progress:", error);
    throw error;
  }
}

//dispatch thunk to get repeat stuck guide progress (if stuck is hit 2 times in a row)
export const thunkRepeatStuckGuideProgress = (vendor) => async (dispatch) => {
  try {
    const res = await fetchWithCSRF(`/api/guide_progress/repeat/${vendor}`);
    if (!res.ok) {
      throw new Error("Failed to fetch guide step progress");
    }
    const data = await res.json();
    if (data.error) {
      throw new Error(data.error);
    }
    dispatch(repeatStuckGuideProgress(data));
    return data;
  } catch (error) {
    console.error("Error fetching guide step progress:", error);
    throw error;
  }
}

// Reducer
// The reducer function takes the current state and an action as arguments
// and returns the new state based on the action type.
// The initial state is an empty object, but you can modify it as needed.
function guideProgressReducer(state = {}, action) {
  switch (action.type) {
    case GET_GUIDE_STEP_PROGRESS:
      return {
        ...state,
        guideStepProgress: action.payload,
      };
    case NEXT_STEP_GUIDE_PROGRESS:
      return {
        ...state,
        guideStepProgress: action.payload,
      };
    case REPEAT_STUCK_GUIDE_PROGRESS:
      return {
        ...state,
        guideStepProgress: action.payload,
      };
    default:
      return state;
  }
}
export default guideProgressReducer;
