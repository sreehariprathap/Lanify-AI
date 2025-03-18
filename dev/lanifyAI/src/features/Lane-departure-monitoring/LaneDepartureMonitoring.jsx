import { useState } from "react";
import axios from "axios";
import LottieFile from "../../components/LottieFile";
import DrivingAnimation from "../../assets/driving.json";
import { Loader, FolderUp } from "lucide-react";

const LaneDepartureMonitoring = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadData, setUploadData] = useState(null);
  const [isUploading, setUploading] = useState(false);

  const handleFileChange = (event) => setSelectedFile(event.target.files[0]);

  const handleUpload = async (event) => {
    event.preventDefault();
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append("video", selectedFile);
    setUploading(true);

    try {
      const response = await axios.post("http://localhost:8080/api/video", formData, {
      headers: { "Content-Type": "multipart/form-data" },
      });
      setUploadData(response.data);
    } catch (error) {
      console.error("Error uploading video:", error);
    }
    setUploading(false);
  };

  const handleReset = () => {
    setSelectedFile(null);
    setUploadData(null);
  };

  return (
    <div className="flex flex-col items-center min-h-screen px-4 py-2">
      <h1 className="text-3xl font-bold text-center">Lane Departure Monitoring</h1>
      <p className="text-center text-gray-600 mt-2">
        Upload a driving video to analyze lane departure events.
      </p>

      {!uploadData && (
        <div className="w-[300px] flex justify-center items-center my-4">
          <LottieFile lottieFile={DrivingAnimation} />
        </div>
      )}

      {!uploadData ? (
        <form className="w-full max-w-md mt-4 flex gap-3" onSubmit={handleUpload}>
          <input
            type="file"
            accept="video/*"
            onChange={handleFileChange}
            className="file-input file-input-primary file-input-lg"
          />
          <button
            type="submit"
            className="btn btn-primary text-white rounded flex gap-2 items-center"
            disabled={isUploading}
          >
            {isUploading ? <Loader className="animate-spin" /> : <FolderUp />}
            {isUploading ? "Uploading..." : "Upload"}
          </button>
        </form>
      ) : (
        <div className="mt-4 w-full max-w-lg">
          <video src={uploadData.videoUrl} controls className="w-full rounded-lg shadow-md" />

          {uploadData.analytics && (
            <div className="space-y-3 mt-4 bg-gray-100 p-4 rounded-lg shadow-md">
              <div className="flex items-center gap-2">
                <span className="font-medium">Driving Alerts:</span>
                <span className="badge badge-error p-1 rounded-full">{uploadData.analytics.total_alerts}</span>
              </div>
              <div>
                <span className="font-medium">Behaviour Summary:</span>
                <p className="text-gray-600">{uploadData.analytics.alerts_summary}</p>
              </div>
              <div>
                <span className="font-medium">Performance Score:</span>
                <p className="text-lg font-bold text-green-600">{uploadData.analytics.safety_score}</p>
              </div>
              <div>
                <span className="font-medium">Improvement Tips:</span>
                <p className="text-gray-600">{uploadData.analytics.recommendations}</p>
              </div>
            </div>
          )}

          <button
            onClick={handleReset}
            className="btn btn-secondary mt-4"
          >
            Upload another video
          </button>
        </div>
      )}
    </div>
  );
};

export default LaneDepartureMonitoring;
