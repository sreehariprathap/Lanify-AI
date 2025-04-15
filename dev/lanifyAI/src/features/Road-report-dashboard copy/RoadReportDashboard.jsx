// import { Map } from '@vis.gl/react-google-maps';
// import { useState } from 'react';
import { useNavigate } from 'react-router';

const RoadReportDashboard = () => {
    const navigate = useNavigate();

    const handleGenerateReport = () => {
        // navigate('/road-assessment');
        // Replace with your logic to generate a report
        console.log('Generate Report button clicked');
    };

    return (
        <div className="p-5 flex gap-2 justify-center">
            {/* <PlaceSearch/> */}
            {/* <MapComponent/> */}
            <button className="btn btn-primary" onClick={handleGenerateReport}>
                Generate Report
            </button>
        </div>
    );
};

export default RoadReportDashboard;
