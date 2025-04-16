/* eslint-disable react/prop-types */
import  { createContext, useContext, useState } from 'react';

const PlaceContext = createContext();

export const PlaceProvider = ({ children }) => {
  const [place, setPlace] = useState(null);

  return (
    <PlaceContext.Provider value={{ place, setPlace }}>
      {children}
    </PlaceContext.Provider>
  );
};

export const usePlace = () => useContext(PlaceContext);
