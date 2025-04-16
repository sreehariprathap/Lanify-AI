/* eslint-disable react/prop-types */
import { useEffect, useState } from 'react';
import { useMap } from '@vis.gl/react-google-maps';

/**
 * RouteHighlighter
 *
 * Queries Google Maps DirectionsService to determine a driving route between the
 * given origin and destination. It extracts the overview polyline and renders a
 * custom Polyline on the map to highlight the road.
 *
 * Props:
 * - origin: string or LatLngLiteral for the starting point.
 * - destination: string or LatLngLiteral for the ending point.
 * - strokeColor: color for the polyline (default: "#00FF00")
 * - strokeWeight: thickness for the polyline (default: 6)
 */
const RouteHighlighter = ({
  origin,
  destination,
  strokeColor = '#00FF00',
  strokeWeight = 6,
}) => {
  const map = useMap();
  const [polyline, setPolyline] = useState(null);

  useEffect(() => {
    if (!map || !window.google || !origin || !destination) return;

    const directionsService = new window.google.maps.DirectionsService();
    directionsService.route(
      {
        origin,
        destination,
        travelMode: window.google.maps.TravelMode.DRIVING,
      },
      (result, status) => {
        if (status === window.google.maps.DirectionsStatus.OK && result.routes.length > 0) {
          const routePath = result.routes[0].overview_path;
          const routePolyline = new window.google.maps.Polyline({
            path: routePath,
            geodesic: true,
            strokeColor,
            strokeOpacity: 1.0,
            strokeWeight,
          });
          routePolyline.setMap(map);
          setPolyline(routePolyline);
        } else {
          console.error('Directions request failed due to ' + status);
        }
      }
    );

    return () => {
      if (polyline) {
        polyline.setMap(null);
      }
    };
  }, [map, origin, destination, strokeColor, strokeWeight]);

  return null;
};

export default RouteHighlighter;
