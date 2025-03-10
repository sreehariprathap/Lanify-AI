import { useEffect } from "react";
import { io } from "socket.io-client";
import LottieFile from "../../components/LottieFile";
import DrivingAnimation from "../../assets/driving.json";
import toast, { Toaster } from 'react-hot-toast';

// Connect to the backend WebSocket server
const socket = io("http://localhost:8080", {
  transports: ["websocket"], // Force WebSocket transport
  reconnectionAttempts: 5,
  timeout: 5000,
});

const LaneDepartureMonitoring = () => {
  useEffect(() => {
    socket.on("connect", () => {
      toast("Connected to WebSocket server");
    });

    socket.on("alertEvent", (data) => {
      toast(`New Event: ${data.message}`, { position: "top-right" });
    });

    socket.on("connect_error", (err) => {
      console.error("WebSocket connection failed:", err);
    });

    return () => {
      socket.off("alertEvent");
      socket.off("connect");
      socket.off("connect_error");
    };
  }, []);

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <div className="w-96">
        <LottieFile lottieFile={DrivingAnimation} />
      </div>
      <div>
        <Toaster />
      </div>
    </div>
  );
};

export default LaneDepartureMonitoring;
