/* eslint-disable react/prop-types */
import { Map } from '@vis.gl/react-google-maps';
import { usePlace } from '../../../context/PlaceContext';
import RouteHighlighter from '../../../components/RoadHighlighter';

const MapView = ({ center, zoom }) => {
  // Define the start and end locations for the route.
  const origin = "299 King St N, Waterloo, ON N2L 3G1";
  const destination = "85 Queen St N, Kitchener, ON N2H 2H1";
  const destnation2 = "227 King St S, Waterloo, ON N2J 1R2"
  const destnation3 = "851 Fischer-Hallman Rd, Kitchener, ON N2M 5N8"

  return (
    <Map
      defaultCenter={center}  // using defaultCenter so the map can be moved after initialization
      defaultZoom={zoom}      // using defaultZoom instead of zoom
      mapContainerStyle={{ width: '100%', height: '100%' }}
      // Enable map dragging and more responsive gesture handling.
      draggableCursor={true}
      options={{
        draggable: true,
        gestureHandling: 'greedy',
        // Offset the visual center by providing top padding
        padding: { top: 50, right: 0, bottom: 0, left: 0 },
      }}
    >
      <RouteHighlighter
        origin={origin}
        destination={destination}
        strokeColor="#FF0000"
        strokeWeight={8}
      />
      <RouteHighlighter
        origin={origin}
        destination={destnation2}
        strokeColor="#FFCC80"
        strokeWeight={8}
      />
      <RouteHighlighter
        origin={origin}
        destination={destnation3}
        strokeColor="#00FF00"
        strokeWeight={8}
      />
    </Map>
  );
};

const RoadReport = () => {
  const { place } = usePlace();
  console.log('place', JSON.stringify(place));

  if (!place) {
    return <div className="p-4">No location information found</div>;
  }

  // Destructure needed properties from the place object.
  const { formatted_address, geometry, name, status } = place;

  // Create a formatted location description.
  const locationDescription = `${formatted_address} – a vibrant region within Waterloo Regional Municipality, Ontario, Canada.`;

  // Dummy data for road analysis.
  const roadAnalysisData = {
    accidents: 12, // Dummy number of accidents due to road issues.
    averageDrivingScore: 7.8, // Dummy average driving score out of 10.
    roadConditionIndex: 65, // Dummy index percentage for road conditions.
  };

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-xl font-bold mb-4">Road Assessment Report</h1>

      {/* Basic location information */}
      <div className="bg-gray-100 p-3 rounded-md">
        {name && (
          <p className="font-medium">
            <strong>Name:</strong> {name}
          </p>
        )}
        {status && (
          <p>
            <strong>Status:</strong> {status}
          </p>
        )}
        {formatted_address && (
          <p>
            <strong>Address:</strong> {formatted_address}
          </p>
        )}
        <p>
          <strong>Location Description:</strong> {locationDescription}
        </p>
      </div>

      {/* Road analysis section with dummy values */}
      <div className="bg-gray-100 p-3 rounded-md">
        <h2 className="text-lg font-semibold mb-2">Road Analysis</h2>
        <p>
          <strong>Number of Accidents (due to road issues):</strong> {roadAnalysisData.accidents}
        </p>
        <p>
          <strong>Average Driving Score:</strong> {roadAnalysisData.averageDrivingScore} / 10
        </p>
        <p>
          <strong>Road Condition Index:</strong> {roadAnalysisData.roadConditionIndex}%
        </p>
      </div>

      {/* Map with highlighted route */}
      {geometry && geometry.location && (
        <div className="mt-4 h-64 w-full border rounded-md overflow-hidden">
          <MapView center={geometry.location} zoom={14} />
        </div>
      )}
    </div>
  );
};

export default RoadReport;
