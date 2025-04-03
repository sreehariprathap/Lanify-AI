import { useState } from 'react';
import { useNavigate } from 'react-router';

const RoadReportDashboard = () => {
    const [locationName, setLocationName] = useState('');
    const [locationDetails, setLocationDetails] = useState('');
    const navigate = useNavigate();

    const handleGenerateReport = () => {
        if (locationName.trim() && locationDetails.trim()) {
            // Passing the values as query parameters
            navigate(`/road-report?name=${encodeURIComponent(locationName)}&details=${encodeURIComponent(locationDetails)}`);
        }
    };

    return (
        <div className="p-5 flex gap-2 justify-center">
            <input
                type="text"
                className="input"
                placeholder="Enter location name"
                value={locationName}
                onChange={(e) => setLocationName(e.target.value)}
            />
            <textarea
                className="input"
                placeholder="Enter location details"
                value={locationDetails}
                onChange={(e) => setLocationDetails(e.target.value)}
            />
            <button className="btn btn-primary" onClick={handleGenerateReport}>
                Generate Report
            </button>
        </div>
    );
};

export default RoadReportDashboard;
