import { fetchWithCSRF } from "../utils/fetchWithCSRF";

const START_GUIDE_STEP = 'guideProgress/START_GUIDE_STEP';
const NEXT_STEP_GUIDE = 'guideProgress/NEXT_STEP_GUIDE';
const REPEAT_STUCK_GUIDE= 'guideProgress/REPEAT_STUCK_GUIDE';

// Action creators
const startGuideStep = (guide) => ({
  type: START_GUIDE_STEP,
  payload: guide,
});
const nextStepGuide = (guide) => ({
  type: NEXT_STEP_GUIDE,
  payload: guide,
});
const repeatStuckGuide = (guide) => ({
  type: REPEAT_STUCK_GUIDE,
  payload: guide,
});
// Thunk action creators
//dispatch thunk to get guide step progress
export const thunkStartGuideStep = (vendor) => async (dispatch) => {
  try {
    const res = await fetchWithCSRF(`/api/guide_progress/start/${vendor}`);
    if (!res.ok) {
      throw new Error("Failed to fetch guide step progress");
    }
    const data = await res.json();
    if (data.error) {
      throw new Error(data.error);
    }
    dispatch(startGuideStep(data));
    return data;
  } catch (error) {
    console.error("Error fetching guide step progress:", error);
    throw error;
  }
}

//dispatch thunk to get next step guide progress
export const thunkNextStepGuide = (vendor) => async (dispatch) => {
  try {
    const res = await fetchWithCSRF(`/api/guide_progress/next/${vendor}`);
    if (!res.ok) {
      throw new Error("Failed to fetch guide step progress");
    }
    const data = await res.json();
    if (data.error) {
      throw new Error(data.error);
    }
    dispatch(nextStepGuide(data));
    return data;
  } catch (error) {
    console.error("Error fetching guide step progress:", error);
    throw error;
  }
}

//dispatch thunk to get repeat stuck guide progress (if stuck is hit 2 times in a row)
export const thunkRepeatStuckGuide = (vendor) => async (dispatch) => {
  try {
    const res = await fetchWithCSRF(`/api/guide_progress/repeat/${vendor}`);
    if (!res.ok) {
      throw new Error("Failed to fetch guide step progress");
    }
    const data = await res.json();
    if (data.error) {
      throw new Error(data.error);
    }
    dispatch(repeatStuckGuide(data));
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
    case START_GUIDE_STEP:
      return {
        ...state,
        guideStep: action.payload,
      };
    case NEXT_STEP_GUIDE:
      return {
        ...state,
        guideStep: action.payload,
      };
    case REPEAT_STUCK_GUIDE:
      return {
        ...state,
        guideStep: action.payload,
      };
    default:
      return state;
  }
}
export default guideProgressReducer;
