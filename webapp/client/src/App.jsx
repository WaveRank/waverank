import { Routes, Route, Link } from "react-router-dom";
import HomePage from "./pages/HomePage";
import AboutPage from "./pages/AboutPage";
import ContributorsPage from "./pages/ContributorsPage";
import CreditsPage from "./pages/CreditsPage";
import "./App.css";


export default function App() {

      return (
        <div className="page">
            <div className="frame">
                <div className="navBar">
                    <h2>WaveRank</h2>

                    <div className="navButtons">
                        <Link to="/about"><button>About</button></Link>
                        <Link to="/contributors"><button>Contributors</button></Link>
                        <Link to="/credits"><button>Credits</button></Link>
                        <Link to="/"><button className="homeButton">Return to Home</button></Link>
                    </div>
                </div>

                <div className="navDivider"></div>

                <div className="header">
                    <div className="headerTitle">
                        <h1>WaveRank</h1>
                        <h1>Audio Classifier</h1>
                    </div>
                    <p>AI-powered audio analysis and music genre classification from sound clips.</p>
                </div>

                <Routes>
                    <Route path="/" element={<HomePage/>}/>
                    <Route path="/about" element={<AboutPage/>}/>
                    <Route path="/contributors" element={<ContributorsPage/>}/>
                    <Route path="/credits" element={<CreditsPage/>}/>
                </Routes>
            </div>
        </div>
    );
};