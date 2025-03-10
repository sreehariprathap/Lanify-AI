import  { useState } from 'react';
import { useNavigate } from 'react-router';

const DrivingReportDashboard = () => {
    const [vehicleId, setVehicleId] = useState('');
    const navigate = useNavigate();

    const handleGenerateReport = () => {
        if (vehicleId.trim()) {
            navigate(`/driving-report/${vehicleId}`);
        }
    };

    return (
        <div className="p-5 flex gap-2 justify-center">
            <input
                type="text"
                className="input"
                placeholder="Enter the vehicle id"
                value={vehicleId}
                onChange={(e) => setVehicleId(e.target.value)}
            />
            <button className="btn btn-primary" onClick={handleGenerateReport}>
                Generate Report
            </button>
        </div>
    );
};

export default DrivingReportDashboard;
