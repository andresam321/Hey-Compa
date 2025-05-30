import { useDispatch, useSelector } from "react-redux"
import { thunkNextStepGuide } from "../../redux/guideProgress"
import { useEffect, useState } from "react"
import StuckHelp from "./StuckHelp";

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
<div className="w-full h-[60vh] bg-[#2a2a32] rounded-xl p-6 shadow-md flex flex-col justify-between items-center text-center text-white">
  <div>
    <p className="font-semibold text-lg text-gray-300">
      Step {currentStepIndex + 1} of {stepTexts.length}
    </p>
    <p className="mt-4 text-2xl font-bold text-white italic">
      {currentInstruction}
    </p>
  </div>

  {!isComplete ? (
    <div className="flex justify-center gap-4 mt-6">
      <button
        onClick={handleNextStep}
        className="px-6 py-3 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition"
      >
        Next Step →
      </button>

      <div className="flex items-center">
        <StuckHelp vendor={vendor} />
      </div>
    </div>
  ) : (
    <p className="mt-6 text-green-400 font-bold">
      🎉 All steps completed!
    </p>
  )}
</div>
  );
};

export default NextStep
