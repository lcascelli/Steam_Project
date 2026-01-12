import { useState } from 'react';



export default function ProjectSection({ project }) {
    const [open, setOpen] = useState(false);

    return (
        <div className="project-section">
            {/* Header */}
            <button 
            className="project-header"
            onClick={() => setOpen(!open)}
            >
                <h2>{project.title}</h2>
                <span>{open ? "-" : "+"}</span>
            </button>

            {/* Body */}
            {open && (
                <div className="project-body"> 
                    <p className="project-description">
                        {project.description}
                    </p>
                    
                    <h4>Tech Stack</h4>
                    <ul className="tech-stack">
                        {project.techstack.map(t => (
                            <li key={t}>{t}</li>
                        ))}
                    </ul>

                    {/* Render type-specific content*/}
                    {project.type === "iframe" && (
                        <iframe
                            src={project.link}
                            title={project.title}
                            width="100%"
                            height="700"
                            loading="lazy"
                            style={{ border: 'none' }}
                            />
                    )}

                    {project.type === "react" && project.component}

                    <div className="project-links">
                        {project.repo && (
                        <a href={project.repo} target="_blank" rel="noopener noreferrer">
                        View Repository
                        </a>
                        )}
                    </div> 
                </div>
            )}
        </div>
    );
}