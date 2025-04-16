/* eslint-disable react/prop-types */
import { Map } from '@vis.gl/react-google-maps';
import { usePlace } from '../../../context/PlaceContext';
import RouteHighlighter from '../../../components/RoadHighlighter';

const MapView = ({ center, zoom = 14 }) => {
  // Define the start and end locations.
  const origin = "299 King St N, Waterloo, ON N2L 3G1";
  const destination = "200 Conestoga Pkwy, Kitchener, ON";

  return (
    <Map
      center={center}
      zoom={zoom}
      mapContainerStyle={{ width: '100%', height: '100%' }}
      // Specify options to enable map dragging and a responsive gesture handling.
      options={{
        draggable: true,
        gestureHandling: 'greedy',
      }}
    >
      <RouteHighlighter
        origin={origin}
        destination={destination}
        strokeColor="#FF0000"
        strokeWeight={8}
      />
    </Map>
  );
};

const RoadReport = () => {
  const { place } = usePlace();

  if (!place) {
    return <div className="p-4">No location information found</div>;
  }

  // Destructure the necessary properties from the place object.
  const { formatted_address, geometry, name, status } = place;

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-xl font-bold mb-4">Road Assessment Report</h1>
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
      </div>

      {geometry && geometry.location && (
        <div className="mt-4 h-64 w-full border rounded-md overflow-hidden">
          <MapView center={geometry.location} zoom={14} />
        </div>
      )}
    </div>
  );
};

export default RoadReport;
