import ProjectSection from "../components/ProjectSection";
import { steamInsights } from "../projects/steamInsights";
import { shinyApp } from "../projects/shinyApp";

function App() {
    const projects = [steamInsights, shinyApp];

    return (
    <div className="portfolio">
        <hi>Projects</hi>

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