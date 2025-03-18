import LaneMonitoringImage from "./assets/lane-detection.png";
import DrivingBehaviorReportImage from "./assets/driving-report.png";
import RoadAssessmentImage from "./assets/road-assesment.png";

import { Link } from "react-router";
import InfoCard from "./components/InfoCard";

function App() {
  return (
    <div className="p-5 flex flex-wrap justify-start gap-5">
      <Link to="/lane-departure-monitoring">
        <InfoCard
          imageUrl={LaneMonitoringImage}
          title="Lane Analytics"
          subtitle="Analyze driving and detect lane departures"
        />
      </Link>
      <Link to="/driving-report-dashboard">
        <InfoCard
          imageUrl={DrivingBehaviorReportImage}
          title="Driving Report"
          subtitle="View driving behaviour reports"
        />
      </Link>
      <Link to="/road-assessment">
        <InfoCard
          imageUrl={RoadAssessmentImage}
          title="Road Assessment"
          subtitle="Review road conditions and assessments"
        />
      </Link>
    </div>
  );
}

export default App;
