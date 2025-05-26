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
      dispatch(thunkGetPaymentGuide(vendor)); // only preload the guide, not start progress yet
    }
  }, [dispatch, vendor]);

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      {/* <h1 className="text-2xl font-bold text-gray-800">Start OCR Steps</h1> */}

      {hasStarted && guideSteps?.length > 0 && (
        <>
          <div className="mt-4 bg-white p-4 rounded shadow-md w-full max-w-md text-center">
            <p className="text-lg text-gray-700 font-medium">
              Step {currentStep + 1}:
            </p>
            <p className="text-gray-600 mt-2">
              {guideSteps[currentStep]}
            </p>
          </div>
        <div>
          <NextStep vendor = {vendor} />
          <StuckHelp vendor = {vendor} />
          </div>
        </>
      )}

      <button
        onClick={handleStartGuideSteps}
        className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Start OCR Steps
      </button>

    </div>
  );
};

export default StartOcrSteps;
