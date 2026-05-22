
import "../styles/contributors.css";

const contributors = [
    {
        name: "Emily Huntley",
        role: "Role",
        description: "Brief description of you/your interests/idk/etc.",
        linkedin: "#",
        github: "#",
    },
    {
        name: "Kevin Klein",
        role: "Role",
        description: "Brief description of you/your interests/idk/etc.",
        linkedin: "#",
        github: "#",
    },
    {
        name: "Madeline Rachow",
        role: "Role",
        description: "Brief description of you/your interests/idk/etc.",
        linkedin: "#",
        github: "#",
    },
    {
        name: "Angela Shin",
        role: "Role",
        description: "Brief description of you/your interests/idk/etc.",
        linkedin: "#",
        github: "#",
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
                                <img className="contributorImage" src="/contributor.png" alt={`${member.name} profile`}/>
                                <p className="contributorRole">{member.role}</p>
                                <p>{member.description}</p>
                                {/* To be replaced with icons */}
                                <div className="contributorLinks">
                                    <a className="contributorLink" href={member.linkedin} target="_blank" rel="noreferrer">LinkedIn</a>
                                    <a className="contributorLink" href={member.github} target="_blank" rel="noreferrer">GitHub</a>
                                </div>
                            </div>
                        </div>
                    ))}
            </div>
        </>
    );
}