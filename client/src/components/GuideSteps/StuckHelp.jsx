import { thunkRepeatStuckGuide } from "../../redux/guideProgress"
import { useDispatch, useSelector } from "react-redux"


const StuckHelp = ({vendor}) => {
  const dispatch = useDispatch();
  const guideData = useSelector((state) => state.guideProgress?.guideStep);
  // const vendor = guideData?.guide_progress?.vendor_name;

  const handleStuckHelp = async () => {
    try {
      if (!vendor) {
        console.error("No vendor detected.");
        return;
      }
      await dispatch(thunkRepeatStuckGuide(vendor));
      console.log("Stuck help fetched successfully for vendor:", vendor);
    } catch (error) {
      console.error("Error fetching stuck help guide:", error);
    }
  }
  return (
    <div>
      <div className="text-center bg-white p-6 rounded shadow max-w-md w-full">
        <p className="text-gray-700 font-semibold text-lg">
          Stuck on a step? 
        </p>
        {/* <p className="mt-2 text-gray-600 text-lg italic">
          If you're stuck, you can repeat the last step for more guidance. CLICK TWICE!
        </p> */}
        <button
          onClick={handleStuckHelp}
          className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Repeat Last Step
        </button>
      </div>
    </div>
  )
}

export default StuckHelp
