import { Routes, Route, NavLink } from "react-router-dom";
import { useState } from 'react';
import HomePage from "./pages/HomePage";
import AboutPage from "./pages/AboutPage";
import ContributorsPage from "./pages/ContributorsPage";
import CreditsPage from "./pages/CreditsPage";
import "./App.css";


export default function App() {
    const [navMenuOpen, setNavMenuOpen] = useState(false);
    const closeMenu = () => setNavMenuOpen(false);
    const getNavLinkClass = ({ isActive }) => isActive ? "navButton active" : "navButton";

      return (
        <div className="page">
            <div className="frame">
                <div className="navBar">
                    <h2>WaveRank</h2>

                    {/* Hamburger nav menu (only for mobile) */}
                    <button className="hamburger" onClick={() => setNavMenuOpen(!navMenuOpen)}>
                        {navMenuOpen ? '✕' : '☰'}
                    </button>

                    <div className={`navButtons ${navMenuOpen ? 'show' : ''}`}>
                        <NavLink to="/about" onClick={closeMenu} className={getNavLinkClass}>About</NavLink>
                        <NavLink to="/contributors" onClick={closeMenu} className={getNavLinkClass}>Contributors</NavLink>
                        <NavLink to="/credits" onClick={closeMenu} className={getNavLinkClass}>Credits</NavLink>
                        <NavLink to="/" onClick={closeMenu} className="homeButton">Return to Home</NavLink>
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
