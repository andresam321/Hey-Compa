import { useDispatch, useSelector } from "react-redux"
import { thunkNextStepGuide } from "../../redux/guideProgress"
import { useEffect, useState } from "react"

const NextStep = ({ vendor }) => {
  const dispatch = useDispatch()
  const [hasStarted, setHasStarted] = useState(false)
//   const guideStepState = useSelector((state) => state.guideProgress.guideStep.current_instruction);
// console.log("🧠 Full guideStep state:", guideStepState);

  const currentInstruction = useSelector((state) => state.guideProgress.guideStep.current_instruction)
  // console.log("currentInstruction:", currentInstruction)
  const guideData = useSelector((state) => state.guideProgress?.guideStep);
  console.log("guideData:", guideData);
  // const vendor = guideData?.guide_progress?.vendor_name;
  console.log("vendor:", vendor);
  const currentStepIndex = guideData?.guide_progress?.current_step;
  console.log("currentStepIndex:", currentStepIndex);
  const stepTexts = guideData?.payment_guide?.step_texts || [];
  console.log("stepTexts:", stepTexts);
  const isComplete = guideData?.guide_progress?.is_complete;
  console.log("isComplete:", isComplete);

  // if (skipFirstStep && currentStepIndex === 0) return null;
  
  const handleNextStep = async () => {
    try {
      if (!vendor) {
        console.error("No vendor detected.");
        return;
      }
      setHasStarted(true);
      await dispatch(thunkNextStepGuide(vendor));
      // console.log("Next step fetched successfully for vendor:", vendor);
      // console.log("Current step index after fetching next step:", currentStepIndex);
    } catch (error) {
      console.error("Error fetching next step guide:", error);
    }
  }

useEffect(() => {
  console.log("✅ Step index updated:", currentStepIndex);
}, [currentStepIndex]);


  const isLastStep = currentStepIndex >= stepTexts.length - 1;
  // console.log("isLastStep:", isLastStep);
  return (
    
    <div className="text-center bg-white p-6 rounded shadow max-w-md w-full">
      <p className="text-gray-700 font-semibold text-lg">
        Step {currentStepIndex + 1} of {stepTexts.length}
      </p>
      <p className="mt-2 text-gray-600 text-lg italic">
        {currentInstruction}
      </p>

      {!isComplete ? (
        <button
          onClick={handleNextStep}
          className="mt-6 px-6 py-3 bg-blue-600 text-white rounded-full hover:bg-blue-700"
        >
          Next Step →
        </button>
      ) : (
        <p className="mt-6 text-green-600 font-bold">
          🎉 All steps completed!
        </p>
      )}
    </div>
  );
};

export default NextStep
