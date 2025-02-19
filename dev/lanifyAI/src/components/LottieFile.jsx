import Lottie from "lottie-react";
import PropTypes from "prop-types";
const LottieFile = ({lottieFile}) => {
  return (
    <Lottie animationData={lottieFile} loop={true} />
  )
}

LottieFile.propTypes = {
  lottieFile: PropTypes.object.isRequired,
};

export default LottieFile
