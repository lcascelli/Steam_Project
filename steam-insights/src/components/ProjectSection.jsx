function ProjectSection({ project }) {
    const [open, setOpen] = useState(false);

    return (
        <div className="project-section">
            <button onClick={() => setOpen(!open)}>
                <h2>{project.title}</h2>
            </button>

            {open && (
                <> 
                    <p>{project.description}</p>
                    
                    <ul>
                        {project.techstack.map(t => (
                            <li key={t}>{t}</li>
                        ))}
                    </ul>
                    {project.type === "iframe" && (
                        <iframe
                            src={project.link}
                            title={project.title}
                            width="100%"
                            height="700"
                            style={{ border: 'none' }}
                            />
                    )}

                    <a href={project.repo} target="_blank">
                        View Repository
                    </a>
                </>
            )}
        </div>
    );
}