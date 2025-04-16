import { useState } from 'react';
import { useNavigate } from 'react-router';
import Autocomplete from "react-google-autocomplete";
import { usePlace } from '../../context/PlaceContext';

const RoadReportDashboard = () => {
    const [locationDetails, setLocationDetails] = useState('');
    const navigate = useNavigate();
    const { setPlace } = usePlace();

    const handleGenerateReport = () => {
        setPlace(locationDetails)
        navigate(`/road-assessment/${locationDetails.place_id}`);
    };


    return (
        <div className="p-5 flex gap-2 justify-center">
            <Autocomplete
                onPlaceSelected={(place) => setLocationDetails(place)}
            />
            <button className="btn btn-primary" onClick={handleGenerateReport}>
                Generate Report
            </button>
        </div>
    );
};

export default RoadReportDashboard;
