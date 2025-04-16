/* eslint-disable react/prop-types */
import  { useEffect, useRef } from "react";
import { useMapsLibrary } from "@vis.gl/react-google-maps";

/**
 * GooglePlacesAutocomplete
 *
 * A reusable component that renders an input field hooked into the Google Places Autocomplete service.
 * The component uses the `useMapsLibrary` hook to load the "places" library.
 *
 * Props:
 * - onPlaceSelect (function): Callback function that receives the place object when a place is selected.
 * - options (object, optional): Additional configuration options for the Autocomplete instance.
 */
const GooglePlacesAutocomplete = ({ onPlaceSelect, options = {} }) => {
  const inputRef = useRef(null);
  // Load the 'places' library from Google Maps
  const places = useMapsLibrary("places");

  useEffect(() => {
    if (!places || !inputRef.current) return;

    // Set default options if not provided
    const defaultOptions = {
      // This defines which fields of the place are returned
      fields: ["geometry", "name", "formatted_address"],
    };

    // Create the autocomplete instance
    const autocomplete = new places.Autocomplete(
      inputRef.current,
      { ...defaultOptions, ...options }
    );

    // Listen for place changes and trigger the callback with the selected place
    const listener = autocomplete.addListener("place_changed", () => {
      const place = autocomplete.getPlace();
      onPlaceSelect(place);
    });

    // Cleanup function if necessary (Google Maps API doesn't provide a direct removeListener method
    // for Autocomplete, but if you manage any subscriptions or other effects, do so here)
    return () => {
      if (listener && listener.remove) {
        listener.remove();
      }
    };
  }, [places, onPlaceSelect, options]);

  return (
    <input
      type="text"
      ref={inputRef}
      placeholder="Search for a place"
      style={{ width: "100%", padding: "8px", fontSize: "14px" }}
    />
  );
};

export default GooglePlacesAutocomplete;
