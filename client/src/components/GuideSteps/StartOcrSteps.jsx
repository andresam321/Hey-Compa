import {useEffect} from 'react'
import { useSelector } from 'react-redux'
import { useDispatch } from 'react-redux'
import { thunkStartGuideStep } from '../../redux/guideProgress';



const StartOcrSteps = () => {

const dispatch = useDispatch();
const currentStep = useSelector((state) => state?.guideProgress?.currentStep);
const vendor = useSelector((state) => state?.guideProgress?.vendor);

const handleStartGuideSteps = async () => {
  try {
    const data = await dispatch(thunkStartGuideStep(vendor));
    console.log("Guide Step Data:", data);
  } catch (error) {
    console.error("Error starting guide steps:", error);
  }
}
useEffect(() => {
  handleStartGuideSteps();
}
, [dispatch, vendor]);

  return (
    <div>
      <div className="flex flex-col items-center justify-center h-screen">
        <h1 className="text-2xl font-bold text-gray-800">Start OCR Steps</h1>
        <p className="text-lg text-gray-600">Current Step: {currentStep}</p>
        <button
          onClick={handleStartGuideSteps}
          className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Start OCR Steps
        </button>
    </div>
  </div>
  )
}

export default StartOcrSteps
