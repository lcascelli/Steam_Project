import './Formats.css'
import ProjectSection from "./components/ProjectSection";
import { steamInsights } from "./projects/steamInsights";
import { PSEOutages } from "./projects/PSEOutages";

function App() {
    const projects = [steamInsights, PSEOutages];

    return (
    <div className="portfolio">
        <hi padding = "8px">Projects</hi>

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
