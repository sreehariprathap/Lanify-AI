import { useEffect } from "react";
import { io } from "socket.io-client";
import LottieFile from "../../components/LottieFile";
import DrivingAnimation from "../../assets/driving.json";

const socket = io("http://localhost:5000");

const LaneDepartureMonitoring = () => {
  useEffect(() => {
    // Listen for the 'alertEvent' from the backend
    socket.on("alertEvent", (data) => {
      alert(`New Event: ${data.message}`);
    });

    // Cleanup on unmount
    return () => {
      socket.off("alertEvent");
    };
  }, []);
  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <div className="w-96">
        <LottieFile lottieFile={DrivingAnimation} />
      </div>
    </div>
  );
};
export default LaneDepartureMonitoring;
