import { useEffect, useState } from 'react';
// import { useParams } from 'react-router-dom';

const DrivingReport = () => {
    const { vehicleId } = 1;
    const [reportData, setReportData] = useState({
        vehicle_id: 1,
        total_alerts: 5,
        alerts_summary: "Harsh braking, Over speeding, Sudden acceleration",
        safety_score: 78,
        recommendations: "Drive at a consistent speed and avoid harsh braking."
    });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (vehicleId) {
            // fetchDrivingReport(1);
        }
    }, [vehicleId]);

    const fetchDrivingReport = async (id) => {
        try {
            // Simulating API response
            const dummyData = {
                vehicle_id: id,
                total_alerts: 5,
                alerts_summary: "Harsh braking, Over speeding, Sudden acceleration",
                safety_score: 78,
                recommendations: "Drive at a consistent speed and avoid harsh braking."
            };
            setTimeout(() => {
                setReportData(dummyData);
                setLoading(false);
            }, 1500);
        } catch (error) {
            console.error('Error fetching driving report:', error);
            setLoading(false);
        }
    };

    // if (!vehicleId) {
    //     return <div className="text-red-500 text-center mt-4">No Vehicle ID provided in the URL.</div>;
    // }

    return (
        <div className="max-w-lg mx-auto p-4">
            <div className="card bg-base-100 shadow-xl p-4">
                <div className="card-body">
                    <h2 className="card-title text-xl font-semibold">Driving Report</h2>
                    <p className="text-gray-500">Vehicle ID: {reportData.id}</p>
                    {loading ? (
                        <div className="flex flex-col gap-2">
                            <div className="skeleton h-6 w-3/4"></div>
                            <div className="skeleton h-4 w-1/2"></div>
                            <div className="skeleton h-4 w-full"></div>
                        </div>
                    ) : reportData ? (
                        <div className="space-y-3">
                            <div className="flex items-center gap-2">
                                <span className="font-medium">Total Alerts:</span>
                                <span className="badge badge-error">{reportData.total_alerts}</span>
                            </div>
                            <div>
                                <span className="font-medium">Alerts Summary:</span>
                                <p className="text-gray-600">{reportData.alerts_summary}</p>
                            </div>
                            <div>
                                <span className="font-medium">Safety Score:</span>
                                <p className="text-lg font-bold text-green-600">{reportData.safety_score}</p>
                            </div>
                            <div>
                                <span className="font-medium">Recommendations:</span>
                                <p className="text-gray-600">{reportData.recommendations}</p>
                            </div>
                        </div>
                    ) : (
                        <p className="text-gray-500">Error loading report.</p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default DrivingReport;
