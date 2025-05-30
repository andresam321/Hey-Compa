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
<div
  className={`w-full bg-blue-100 text-blue-900 rounded-lg px-6 py-4 shadow-sm ${
    hasStarted ? 'h-full' : ''
  }`}
>
  {!hasStarted && (
    <div className="text-right">
      <button
        onClick={handleStartGuideSteps}
        className="bg-blue-600 text-white px-4 py-2 rounded-full hover:bg-blue-700 transition"
      >
        Start OCR Steps
      </button>
    </div>
  )}

  {hasStarted && guideSteps?.length > 0 && (
    <>
      <h2 className="text-base font-semibold mb-2">{vendor}</h2>
      {/* <div className="flex flex-col h-full"> */}
        <div className="h-full w-full">
          <NextStep vendor={vendor} />
        </div>
    {/* </div> */}
    </>
  )}
</div>

  );
};


export default StartOcrSteps;
