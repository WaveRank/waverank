import { FaGithub, FaLinkedin } from "react-icons/fa";
import "../styles/contributors.css";

const contributors = [
    {
        name: "Emily Huntley",
        image: "/Emily.jpg",
        role: "YouTube Integration Engineer & Assistant ML Trainer",
        description: [
            "Emily currently works in the 3D printing research industry, where she developed a love for problem-solving and technical precision that led her to a new passion in software engineering. ",
            "She is completing the Oregon State University Post-Baccalaureate Computer Science program, where she honed her skills in full-stack development, machine learning, and systems programming. ",
            "On this project, Emily served as the YouTube Integration Engineer and Assistant ML Trainer, contributing to both the backend pipeline and model development. ",
            "Outside of tech, she resides in sunny Albuquerque, NM, and spends as many weekends as possible exploring the mountains. ",
            "She is actively seeking software engineering roles and would love to connect!"
        ],
        linkedin: "https://www.linkedin.com/in/emilyfhuntley/",
        github: "https://github.com/emilyfhuntley",
    },
    {
        name: "Kevin Klein",
        image: "/Kevin.jpg",
        role: "Backend Engineer",
        description: [
            "Kevin is completing the Oregon State University Post-Baccalaureate Computer Science program and will continue his studies through Georgia Tech's Online Master of Science in Computer Science program. ",
            "His interests include backend or full-stack development, systems programming, and performance-oriented software engineering. On this project, Kevin focused primarily on backend development, ",
            "including API design, file processing and verification, visualization generation, and inference pipeline integration. Outside of software engineering, Kevin lives in Taiwan, where he works as an ",
            "English teacher and enjoys exploring the countryside by scooter. He is seeking software engineering internship opportunities and welcomes professional connections."
        ],
        linkedin: "#",
        github: "https://github.com/KevKlein",
    },
    {
        name: "Madeline Rachow",
        image: "/Madeline.jpg",
        role: "Frontend Engineer",
        description: [
            "Madeline is a Computer Science student at Oregon State University with a strong foundation in full-stack development, applied machine learning, and systems programming. ",
            "She has conducted multi-year undergraduate research at the University of Texas at Dallas and the University of Arkansas, working with large-scale biometric datasets and developing fusion models for face, body, and gait recognition. ",
            "In recent projects, she contributed to both frontend and backend systems, including leading initial model development and implementing full-stack interfaces for interactive applications. ",
            "She is transitioning toward cybersecurity-focused graduate study through Georgia Tech OMSCS and is open to software engineering and security-related roles.",
        ],
        linkedin: "#",
        github: "https://github.com/MadelineRachow",
    },
    {
        name: "Angela Shin",
        image: "/Angie.png",
        role: "Head ML Engineer",
        description: [
            "Angela is completing the Oregon State University Post-Baccalaureate Computer Science program where she was able to develop skills in full-stack development, systems programming, machine learning, ",
            "and mobile development. As part of this project, she primarily focused on model training and development, conducting experiments to improve model accuracy and generalization alongside some backend development ",
            "work. She is particularly interested in model optimization, training strategies, and deep learning theory. In her free time, she loves to go on hikes and is an avid reader. She plans to pursue graduate studies ",
            "in machine learning and is open to software engineering and ML engineer roles."
        ],
        linkedin: "#",
        github: "https://github.com/angshin",
    },
];

export default function ContributorsPage() {
    return (
        <>
            <div className="header">
                <div className="headerTitle">
                    <h1>WaveRank</h1>
                    <h1>Contributors</h1>
                </div>
                <p>The team behind WaveRank and its audio intelligence system.</p>
            </div>
            <div className="contributorsGrid">
                {contributors.map((member, index) => (
                        <div className="contributorsContainer" key={index}>
                            <h3 className="contributorsHeader">{member.name}</h3>
                            <div className="contributorsContent">
                                <img className="contributorImage" src={member.image} alt={`${member.name} profile`}/>
                                <p className="contributorRole">{member.role}</p>
                                <p>{member.description}</p>
                                {/* To be replaced with icons */}
                                <div className="contributorLinks">
                                    {member.linkedin && member.linkedin !== "#" && (<a className="contributorLink" href={member.linkedin} target="_blank" rel="noreferrer"><FaLinkedin/></a>)}
                                    {member.github && member.github !== "#" && (<a className="contributorLink" href={member.github} target="_blank" rel="noreferrer"><FaGithub/></a>)}
                                </div>
                            </div>
                        </div>
                    ))}
            </div>
        </>
    );
}