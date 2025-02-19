import { Link } from "react-router";
import lanifyLogo from "../assets/lanify-1.png";

const Navbar = () => {
  return (
    <div className="navbar bg-base-100 shadow-sm px-5">
      <div className="flex-1">
        <Link to="/">
          <img src={lanifyLogo} alt="lanify logo" className="w-44" />
        </Link>
      </div>
      <div className="flex-none">
        <ul className="menu menu-horizontal px-1">
          <li>
            <a>About</a>
          </li>
          <li>
            <details>
              <summary>More &nbsp;</summary>
              <ul className="bg-base-100 rounded-t-none p-2">
                <li>
                  <a>Contact</a>
                </li>
                <li>
                  <a>Github</a>
                </li>
              </ul>
            </details>
          </li>
        </ul>
      </div>
    </div>
  );
};
export default Navbar;
