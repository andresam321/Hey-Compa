import { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { thunkStartGuideStep } from '../../redux/guideProgress';
import { thunkGetPaymentGuide } from '../../redux/paymentGuide';
import NextStep from './NextStep';
import StuckHelp from './StuckHelp';

const StartOcrSteps = ({vendor}) => {
  const dispatch = useDispatch();
  console.log("vendor line 10:", vendor);
  // const vendorFromDoc = useSelector((state) => state.document?.vendor_detected);
  // const guideData = useSelector((state) => state.guideProgress?.guideStep);
  // console.log("guideData:", guideData);
  const guideSteps = useSelector((state) => state.paymentGuide?.paymentGuide?.step_texts);
  const currentStep = useSelector((state) => state.guideProgress?.guideStep?.guide_progress?.current_step);
  console.log('currentStep:', currentStep);
  console.log('guideSteps:', guideSteps);
  const currentInstruction = useSelector((state) => state?.guideProgress?.guideStep?.current_instruction)
  console.log("currentInstruction line 15:", currentInstruction)
  const [hasStarted, setHasStarted] = useState(false); 
  const [skipFirstStep, setSkipFirstStep] = useState(false); // state to control skipping the first step

  const handleStartGuideSteps = async () => {
    try {
      await dispatch(thunkStartGuideStep(vendor));
      console.log("Guide steps started successfully for vendor:", vendor);
      // show the first step
      setHasStarted(true);
    } catch (error) {
      console.error("Error starting guide steps:", error);
    }
  };
  
  useEffect(() => {
  if (vendor) {
    dispatch(thunkStartGuideStep(vendor));
    dispatch(thunkGetPaymentGuide(vendor));
  }
}, [dispatch, vendor]);

  useEffect(() => {
    if (vendor) {
      dispatch(thunkGetPaymentGuide(vendor)); // only preload the guide, not start progress yet
    }
  }, [dispatch, vendor]);

  return (
    <div className="flex flex-col items-start space-y-4 mt-6">

      {/* Button as user message */}
      {!hasStarted && (
        <div className="self-end max-w-[75%]">
          <button
            onClick={handleStartGuideSteps}
            className="bg-blue-600 text-white px-4 py-2 rounded-full hover:bg-blue-700"
          >
            Start OCR Steps
          </button>
        </div>
      )}

      {/* Display guide step like bot message */}
      {hasStarted && guideSteps?.length > 0 && (
        <div className="bg-gray-200 text-gray-800 rounded-lg px-4 py-3 max-w-[75%] self-start whitespace-pre-wrap">
          <p className="text-sm font-semibold">Step {currentStep + 1}:</p>
          <p className="text-sm mt-1">{guideSteps[currentStep]}</p>
          <h2> {vendor} </h2>
          <div className="mt-4">
            <NextStep vendor={vendor} />
            <StuckHelp vendor={vendor} />
          </div>
        </div>
      )}
    </div>
  );
};


export default StartOcrSteps;
