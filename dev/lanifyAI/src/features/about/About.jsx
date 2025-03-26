import { GithubIcon, LinkedinIcon } from "lucide-react";
import lanifyPoster from "../../assets/lanify-poster.png";

const About = () => {
    return (
        <section className="min-h-screen bg-gray-100 flex items-center justify-center p-6">
            <div className="flex flex-col md:flex-row w-full max-w-6xl">
                {/* Left Side: Image */}
                <div className="w-full md:w-1/2 flex justify-center items-center p-4">
                    <img
                        src={lanifyPoster}
                        alt="App Poster"
                        className="w-full max-w-md object-contain"
                    />
                </div>
                {/* Right Side: Content */}
                <div className="w-full md:w-1/2 flex flex-col gap-8 p-4">
                    <div className="card bg-base-100 shadow-xl">
                        <div className="card-body">
                            <h2 className="card-title text-2xl font-bold">
                                Video-Based Lane Detection System
                            </h2>
                            <p>
                                Our affordable aftermarket AI system brings advanced lane departure
                                warnings to budget-conscious drivers. Simply upload a driving video,
                                and our ML model will analyze lane discipline, detect driving mistakes,
                                and highlight potential road issues such as poor lane markings or unsafe
                                departures. This solution empowers all drivers with real-time safety
                                insights, enhancing road awareness without the high cost of premium vehicles.
                            </p>
                        </div>
                    </div>
                    <div className="card bg-base-100 shadow-xl">
                        <div className="card-body">
                            <h2 className="card-title text-2xl font-bold">
                                Smart Driving and Road Safety Analytics Platform
                            </h2>
                            <p>
                                Our AI-powered platform leverages data from uploaded driving videos to
                                assess both driver behavior and road conditions. By analyzing lane
                                discipline, driving errors, and road quality, the system generates a
                                comprehensive dashboard that assigns driving scores for individuals—ideal
                                for driving schools, new drivers, or assessment programs. Simultaneously,
                                it identifies road maintenance needs, helping authorities prioritize
                                infrastructure improvements. This dual-purpose solution enhances driver
                                safety and supports smarter road maintenance strategies.
                            </p>
                        </div>
                    </div>
                    <div className="flex justify-center gap-4">
                        <a href="https://github.com" target="_blank" rel="noopener noreferrer">
                            <GithubIcon className="h-6 w-6 text-gray-700 hover:text-gray-900" />
                        </a>
                        <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer">
                            <LinkedinIcon className="h-6 w-6 text-blue-700 hover:text-blue-900" />
                        </a>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default About;
