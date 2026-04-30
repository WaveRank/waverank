import { Routes, Route, Link } from "react-router-dom";
import HomePage from "../pages/HomePage";
import AboutPage from "../pages/AboutPage";
import ContributorsPage from "../pages/ContributorsPage";
import CreditsPage from "../pages/CreditsPage";
import "./App.css";

export default function App() {
    return (
        <div>
            <div className="navBar">
                <h1>WaveRank</h1>

                <div className="navButtons">
                    <Link to="/about"><button>About</button></Link>
                    <Link to="/contributors"><button>Contributors</button></Link>
                    <Link to="/credits"><button>Credits</button></Link>
                    <Link to="/"><button className="homeButton">Home</button></Link>
                </div>
            </div>

            <div className="header">
                <h1>WaveRank</h1>
                <p>AI-powered music genre classification from audio clips</p>
            </div>

            <Routes>
                <Route path="/" element={<HomePage/>}/>
                <Route path="/about" element={<AboutPage/>}/>
                <Route path="/contributors" element={<ContributorsPage/>}/>
                <Route path="/credits" element={<CreditsPage/>}/>
            </Routes>
        </div>
    );
};