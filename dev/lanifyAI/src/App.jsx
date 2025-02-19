import LaneDepartureImage from "./assets/0x0.jpg";
import { Link } from "react-router";

function App() {
  return (
    <div className="p-5">
      <Link to="/lane-departure-monitoring">
        <div className="group group-hover:card group-hover:image-full relative w-96 shadow-sm rounded-lg">
          <figure className="overflow-hidden">
            <img
              className="w-full  transition-transform duration-300 ease-in-out group-hover:scale-105 rounded-lg"
              src={LaneDepartureImage}
              alt="Lane Departure"
            />
          </figure>
          <div className="absolute inset-0 flex items-center justify-center bg-base-50 bg-opacity-70 transition-opacity duration-300 ease-in-out ">
            <div className="text-center flex flex-col items-center">
              <h2 className="card-title text-white font-bold text-center text-4xl ">Monitor lanes</h2>
              <p className=" opacity-0 group-hover:opacity-100 text-white shadow-sm">
                Get realtime lane departure alerts
              </p>
            </div>
          </div>
        </div>
      </Link>
    </div>
  );
}

export default App;
