import PropTypes from "prop-types";
import Navbar from "../components/Navbar";
const MainLayout = ({ children }) => {
  return (
    <div className="flex flex-col">
      <Navbar />
      {children}
    </div>
  );
};

MainLayout.propTypes = {
  children: PropTypes.node.isRequired,
};

export default MainLayout;
