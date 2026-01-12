import './Formats.css'
import ProjectSection from "./components/ProjectSection";
import { steamInsights } from "./projects/steamInsights";
import { PSEOutages } from "./projects/PSEOutages";

function App() {
    const projects = [steamInsights, PSEOutages];

    return (
    <div className="portfolio">
        <h1 className="portfolio-header">Projects List</h1>
          <h2 className='portfolio-subheader'>Click on a project title to view</h2>

      {projects.map(project => (
        <ProjectSection 
        key={project.id} 
        project={project} 
        />
      ))}
    </div>
  );
}

export default App;
