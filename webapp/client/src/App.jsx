import { Routes, Route, NavLink } from "react-router-dom";
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
                        <NavLink to="/about" className={({ isActive }) => isActive ? "navButton active" : "navButton"}>About</NavLink>
                        <NavLink to="/contributors" className={({ isActive }) => isActive ? "navButton active" : "navButton"}>Contributors</NavLink>
                        <NavLink to="/credits" className={({ isActive }) => isActive ? "navButton active" : "navButton"}>Credits</NavLink>
                        <NavLink to="/" className="homeButton">Return to Home</NavLink>
                    </div>
                </div>

                <div className="navDivider"></div>

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
